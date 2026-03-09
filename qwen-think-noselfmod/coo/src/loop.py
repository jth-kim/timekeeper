"""
Timekeeper COO — Main Agent Loop

Continuous thinking architecture:
- Data fetch: every CHECK_INTERVAL_SECONDS (default 30 min)
- Think cycles: back-to-back with a brief cooldown (default 60s)
- The LLM takes as long as it needs per cycle; depth is controlled by
  token budget (num_predict), not wall-clock scheduling.

Mode selection is influenced by time of day — quiet hours favor investigation
and deep thinking; active hours favor observation.

When data is stale (unchanged for multiple cycles), observe/hypothesize modes
are automatically diverted to investigate mode, where the COO writes and runs
Python scripts to produce novel analytical results.
"""

import asyncio
import hashlib
import json
import time
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

import httpx
import structlog

import config
import memory
from supabase_client import (
    get_current_timer,
    get_recent_entries,
    load_state,
    save_state,
)
from ollama_client import think, select_mode
from signal_client import send_message


# --- Mode schedules ---

# Active hours (06:00-23:00): balanced — observe for fresh data, investigate/hypothesize for depth
ACTIVE_SCHEDULE = {
    0: "observe",
    1: "investigate",
    2: "reflect",
    3: "observe",
    4: "hypothesize",
    5: "investigate",
    6: "critique",
    7: "observe",
    8: "plan",
    9: "investigate",
    10: "evolve",
    11: "observe",
}

# Quiet hours (23:00-06:00): investigation-heavy, deep thinking, self-evolution
QUIET_SCHEDULE = {
    0: "investigate",
    1: "investigate",
    2: "hypothesize",
    3: "investigate",
    4: "critique",
    5: "investigate",
    6: "investigate",
    7: "evolve",
}


def _local_timestamper(logger, method, event_dict):
    """Structlog processor that stamps events in the user's local timezone."""
    try:
        tz = ZoneInfo(config.USER_TIMEZONE)
    except Exception:
        tz = timezone.utc
    event_dict["timestamp"] = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S %Z")
    return event_dict


def _setup_logging():
    """Configure structured JSON logging."""
    config.LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_file = open(config.LOG_DIR / "coo.jsonl", "a")

    structlog.configure(
        processors=[
            _local_timestamper,
            structlog.processors.add_log_level,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.BoundLogger,
        logger_factory=structlog.WriteLoggerFactory(file=log_file),
    )


def _is_active_hours() -> bool:
    """Check if we're in the user's active hours."""
    try:
        tz = ZoneInfo(config.USER_TIMEZONE)
    except Exception:
        tz = timezone.utc
    local_hour = datetime.now(tz).hour
    return config.ACTIVE_HOURS_START <= local_hour < config.ACTIVE_HOURS_END


def _local_time_str() -> str:
    """Get a human-readable local time string for the user's timezone."""
    try:
        tz = ZoneInfo(config.USER_TIMEZONE)
    except Exception:
        tz = timezone.utc
    now = datetime.now(tz)
    return now.strftime("%A %H:%M %Z")


def _data_fingerprint(timer: dict | None, entries: list[dict]) -> str:
    """Create a fingerprint of the current data to detect changes."""
    content = json.dumps({"timer": timer, "entries": entries}, sort_keys=True, default=str)
    return hashlib.sha256(content.encode()).hexdigest()[:16]


def _format_timer(timer: dict | None) -> str:
    """Format current timer state for the LLM context."""
    if not timer or not timer.get("is_running"):
        return "No timer currently running."

    parts = [f"Currently tracking: {timer.get('project_name', 'unknown')}"]
    if timer.get("client_name"):
        parts.append(f"Client: {timer['client_name']}")
    if timer.get("description"):
        parts.append(f"Description: {timer['description']}")
    if timer.get("tags"):
        tags = timer["tags"] if isinstance(timer["tags"], list) else [timer["tags"]]
        parts.append(f"Tags: {', '.join(str(t) for t in tags)}")
    if timer.get("start"):
        parts.append(f"Started: {timer['start']}")
    if timer.get("elapsed_seconds_at_sync"):
        mins = round(timer["elapsed_seconds_at_sync"] / 60)
        parts.append(f"Elapsed: ~{mins} minutes (at last sync)")

    return "\n".join(parts)


def _format_entries(entries: list[dict]) -> str:
    """Format recent entries for the LLM context."""
    if not entries:
        return "No recent time entries."

    lines = [f"Recent entries ({len(entries)} in last 48h):"]
    for e in entries[:20]:
        client = e.get("client_name", "?")
        project = e.get("project_name", "?")
        tags = e.get("tags", [])
        tag_str = f" [{', '.join(str(t) for t in tags)}]" if tags else ""
        duration = e.get("duration", "?")
        start = e.get("start", "?")
        lines.append(f"  {start} | {client} / {project}{tag_str} | {duration}")

    return "\n".join(lines)


def _build_data_context(timer: dict | None, entries: list[dict], unchanged_cycles: int = 0, cycle_count: int = 0) -> str:
    """Assemble the time-tracking data context string."""
    now = datetime.now(timezone.utc)
    active = _is_active_hours()
    local_time = _local_time_str()

    parts = [
        _format_timer(timer),
        "",
        _format_entries(entries),
        "",
        f"Current time (UTC): {now.isoformat()}",
        f"Local time: {local_time}",
        f"Day of week: {now.strftime('%A')}",
        f"Posture: {'ACTIVE HOURS — user may be working' if active else 'QUIET HOURS — user is likely offline. This is your time for deep thinking and investigation.'}",
        f"Cycle count (this session): {cycle_count}",
    ]

    thresholds = config.load_thresholds()
    if thresholds:
        parts.append("")
        parts.append(f"Alert thresholds config: {json.dumps(thresholds)}")

    if unchanged_cycles >= config.STALE_CYCLE_THRESHOLD:
        parts.append("")
        parts.append(f"⚠ DATA STALENESS: This data is UNCHANGED for {unchanged_cycles} consecutive cycles. You have ALREADY described this data multiple times. Do NOT re-describe it. Do NOT recompute the same arithmetic. Instead: explore a new angle, question an assumption, connect two things you haven't connected before, or investigate something you can't see in the raw data.")

    return "\n".join(parts)


def _build_activity_trail() -> str:
    """Build a compact trail of recent cycle activity for orientation.

    Reads the last 8 journal entries and extracts a one-line summary of each,
    giving the COO a sense of 'what I've been doing' across cycles.
    """
    recent = memory.read_recent("journal.md", n=8)
    if not recent:
        return ""

    from memory import _split_entries
    entries = _split_entries(recent)

    lines = []
    for entry in entries:
        # Extract timestamp and first meaningful line
        entry_lines = entry.strip().split("\n")
        timestamp = ""
        summary = ""
        for line in entry_lines:
            line = line.strip()
            if line.startswith("### "):
                timestamp = line.replace("### ", "")
                continue
            if not line:
                continue
            # First non-empty, non-header line is the summary
            # Strip markdown bold markers for compactness
            summary = line.replace("**", "").strip()
            # Truncate long summaries
            if len(summary) > 120:
                summary = summary[:117] + "..."
            break

        if timestamp and summary:
            lines.append(f"- {timestamp}: {summary}")

    if not lines:
        return ""
    return "## Where You Left Off\nYour recent activity (oldest → newest):\n" + "\n".join(lines) + \
           "\n\nUse this to orient yourself. Continue a thread, build on a finding, or deliberately change direction — but know where you've been."


def _build_memory_context(mode: str, stale_cycles: int = 0) -> str:
    """Build unified memory context. Every mode sees all memory, with emphasis based on mode.

    When data is stale, reduce context to break the echo chamber — show fewer
    journal entries and skip priorities for reflect mode.
    """
    sections = []
    is_stale = stale_cycles >= config.STALE_CYCLE_THRESHOLD

    # --- Activity trail (orientation) — always first ---
    trail = _build_activity_trail()
    if trail:
        sections.append(trail)

    # --- Last entry (explicit continuity prompt) ---
    journal = memory.read_recent("journal.md", n=1)
    if journal:
        if is_stale:
            sections.append(f"## Your Most Recent Thought\n{journal}\n\n(Data is stale. Do NOT repeat this. Think about something DIFFERENT.)")
        else:
            sections.append(f"## Your Most Recent Thought\n{journal}\n\n(Build on this or move past it. Do not restate it.)")

    # --- Message from the Sovereign ---
    sovereign_msg = memory.read_file("sovereign.md")
    if sovereign_msg.strip():
        sections.append(f"## Message from the Sovereign\nThe Sovereign has written you a direct message. This file is READ-ONLY for you — only the Sovereign can write to it. Read it carefully and incorporate it into your thinking. If you want to respond, do so through your journal or by setting should_act=true.\n\n{sovereign_msg}")

    # --- Agenda (unfinished business) ---
    agenda = memory.read_file("agenda.md")
    if agenda.strip():
        sections.append(f"## Your Agenda (questions and threads to pursue)\n{agenda}")
    else:
        sections.append("## Your Agenda\n(Empty — you have not set carry-forward questions yet. Use the 'agenda' field in your response to set 2-3 specific questions for your next cycle.)")

    # --- Full journal (reduced when stale to break echo) ---
    if is_stale:
        n_journal = 3  # Only last 3 when stale — enough for continuity, not enough to echo
    else:
        n_journal = 5 if mode == "observe" else 10
    full_journal = memory.read_recent("journal.md", n=n_journal)
    if full_journal:
        sections.append(f"## Recent Journal ({n_journal} entries)\n{full_journal}")

    # --- Priorities (skip for reflect when stale to prevent anchoring) ---
    if not (is_stale and mode == "reflect"):
        priorities = memory.read_file("priorities.md")
        if priorities.strip():
            sections.append(f"## Current Priorities\n{priorities}")

    # --- Recent reflections (skip when stale to reduce self-reference) ---
    if not is_stale:
        reflections = memory.read_recent("reflections.md", n=3)
        if reflections:
            sections.append(f"## Recent Reflections\n{reflections}")

    # --- Always include active hypotheses ---
    hyp = memory.read_recent("hypotheses.md", n=5)
    if hyp:
        sections.append(f"## Active Hypotheses\n{hyp}")

    # --- Recent investigations ---
    investigations = memory.read_recent("investigations.md", n=3)
    if investigations:
        sections.append(f"## Recent Investigations\n{investigations}")

    # --- Self-model (always available, but especially important for evolve) ---
    self_model = memory.read_file("self_model.md")
    if self_model.strip():
        sections.append(f"## Your Self-Model\n{self_model}")

    # --- Mode-specific extras ---
    if mode == "critique":
        critique = memory.read_recent("self_critique.md", n=3)
        if critique:
            sections.append(f"## Previous Self-Critiques\n{critique}")

    elif mode == "evolve":
        # Operational logs for self-diagnosis
        recent_logs = memory.read_recent_logs(n=15)
        if recent_logs:
            sections.append(f"## Recent Operational Logs\n```\n{recent_logs}\n```")
        # Current editable config files
        for cfg_name in sorted(memory.EDITABLE_CONFIGS):
            cfg_content = memory.read_config(cfg_name)
            if cfg_content:
                sections.append(f"## Current Config: {cfg_name}\n```markdown\n{cfg_content}\n```")
        # Self-critique for context
        critique = memory.read_recent("self_critique.md", n=3)
        if critique:
            sections.append(f"## Recent Self-Critiques\n{critique}")

    return "\n\n".join(sections) if sections else ""


def _build_workspace_context() -> str:
    """Build context about the workspace for investigate mode."""
    from sandbox import list_tools, get_script_history

    parts = []

    tools = list_tools()
    if tools:
        tool_lines = "\n".join(f"- `{t['name']}`: {t['description']} (updated {t['last_modified']})" for t in tools)
        parts.append(f"### Your Tools (in /data/workspace/tools/)\n{tool_lines}")

    history = get_script_history(n=8)
    if history:
        parts.append(f"### Recent Investigations (DO NOT repeat these)\n{history}")

    if not parts:
        parts.append("### Workspace\nNo previous investigations. This is your first — start with something foundational.")

    return "\n\n".join(parts)


def _get_scheduled_mode(cycle_count: int) -> str:
    """Get the default mode from the rotation schedule, adjusted for time of day."""
    active = _is_active_hours()
    schedule = ACTIVE_SCHEDULE if active else QUIET_SCHEDULE
    idx = cycle_count % len(schedule)
    return schedule[idx]


def _to_str(value) -> str:
    """Coerce a value to string — handles dicts/lists from LLM JSON responses."""
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        # Format dict as readable bullet points
        lines = []
        for k, v in value.items():
            lines.append(f"- **{k}**: {v}")
        return "\n".join(lines)
    if isinstance(value, list):
        return "\n".join(f"- {item}" for item in value)
    return str(value)


def _compose_structured_entry(sections: list[tuple[str, str | dict]]) -> str:
    """Compose structured thinking sections into a readable markdown entry."""
    parts = []
    for label, content in sections:
        text = _to_str(content)
        if text.strip():
            parts.append(f"**{label}**:\n{text.strip()}" if "\n" in text else f"**{label}**: {text.strip()}")
    return "\n\n".join(parts)


def _save_thought_to_memory(mode: str, result: dict) -> None:
    """Write the structured thinking result to the appropriate memory files."""
    # Save agenda if the LLM included one
    next_agenda = result.get("agenda", "")
    if next_agenda:
        memory.write_file("agenda.md", _to_str(next_agenda))

    if mode == "observe":
        entry = _compose_structured_entry([
            ("Ground", result.get("ground", "")),
            ("Tension", result.get("tension", "")),
            ("Synthesis", result.get("synthesis", "")),
        ])
        # Fallback for unstructured responses
        if not entry.strip():
            entry = result.get("observation", result.get("internal_note", ""))
        if entry.strip():
            memory.append_entry("journal.md", entry)

    elif mode == "reflect":
        entry = _compose_structured_entry([
            ("Ground", result.get("ground", "")),
            ("Tension", result.get("tension", "")),
            ("Possibility", result.get("possibility", "")),
            ("Synthesis", result.get("synthesis", "")),
        ])
        # Fallback
        if not entry.strip():
            entry = result.get("reflection", "")
        if entry.strip():
            memory.append_entry("reflections.md", entry)
            memory.append_entry("journal.md", f"[reflect]\n\n{entry}")

    elif mode == "plan":
        entry = _compose_structured_entry([
            ("Situation", result.get("situation", "")),
            ("Tensions", result.get("tensions", "")),
            ("Intentions", result.get("intentions", "")),
            ("Self-Check", result.get("self_check", "")),
        ])
        # Fallback
        if not entry.strip():
            entry = result.get("priorities", "")
        if entry.strip():
            memory.write_file("priorities.md", entry)
            memory.append_entry("journal.md", f"[plan]\n\n{entry}")

    elif mode == "critique":
        entry = _compose_structured_entry([
            ("Claim", result.get("claim", "")),
            ("Evidence Against", result.get("evidence_against", "")),
            ("Verdict", result.get("verdict", "")),
            ("Correction", result.get("correction", "")),
        ])
        # Fallback
        if not entry.strip():
            entry = result.get("critique", "")
        if entry.strip():
            memory.append_entry("self_critique.md", entry)
            memory.append_entry("journal.md", f"[critique]\n\n{entry}")

    elif mode == "hypothesize":
        status = _to_str(result.get("status", "new"))
        entry = _compose_structured_entry([
            ("Observation", result.get("observation", "")),
            ("Hypothesis", result.get("hypothesis", "")),
            ("Evidence", result.get("evidence", "")),
            ("Falsification", result.get("falsification", "")),
            ("Stakes", result.get("stakes", "")),
        ])
        # Fallback
        if not entry.strip():
            entry = _to_str(result.get("hypothesis", ""))
        if entry.strip():
            memory.append_entry("hypotheses.md", f"[{status}]\n\n{entry}")
            memory.append_entry("journal.md", f"[hypothesis:{status}]\n\n{entry}")

    elif mode == "evolve":
        # Update self-model
        self_model = _to_str(result.get("self_model", ""))
        if self_model.strip():
            memory.write_file("self_model.md", self_model)

        # Apply config edits
        config_edits = result.get("config_edits", [])
        if config.SELF_MOD_ENABLED and isinstance(config_edits, list):
            for edit in config_edits:
                if isinstance(edit, dict):
                    fname = edit.get("file", "")
                    content = _to_str(edit.get("content", ""))
                    desc = _to_str(edit.get("description", ""))
                    if fname and content.strip():
                        success = memory.write_config(fname, content)
                        status_str = "applied" if success else "rejected (not in allow-list or read-only)"
                        memory.append_entry("journal.md",
                            f"[evolve:config] Edited {fname}: {desc} — {status_str}")
        elif not config.SELF_MOD_ENABLED and config_edits:
            memory.append_entry("journal.md", "[evolve:config] Self-mod disabled in this run; skipped proposed config edits.")

        # Journal the operational notes and self-model update
        op_notes = _to_str(result.get("operational_notes", ""))
        journal_parts = ["[evolve]"]
        if self_model.strip():
            journal_parts.append("Updated self-model.")
        if op_notes.strip():
            journal_parts.append(f"Operational notes: {op_notes}")
        if config_edits:
            journal_parts.append(f"Config edits attempted: {len(config_edits)}")
        memory.append_entry("journal.md", "\n\n".join(journal_parts))


def _save_investigation_to_memory(gen_result: dict, exec_result: dict, interp_result: dict) -> None:
    """Save investigation results to memory."""
    question = _to_str(gen_result.get("question", ""))
    script_name = _to_str(gen_result.get("script_name", ""))
    finding = _to_str(interp_result.get("finding", ""))
    significance = _to_str(interp_result.get("significance", ""))
    next_q = _to_str(interp_result.get("next_question", ""))
    success = exec_result.get("success", False)

    # Save to dedicated investigations file
    inv_entry = _compose_structured_entry([
        ("Question", question),
        ("Script", script_name),
        ("Result", "Success" if success else "Failed"),
        ("Finding", finding),
        ("Significance", significance),
        ("Next Question", next_q),
    ])
    if inv_entry.strip():
        memory.append_entry("investigations.md", inv_entry)

    # Also journal it
    journal_entry = f"[investigate] {question}\n\n"
    if success:
        journal_entry += f"**Finding**: {finding}\n\n**Significance**: {significance}"
    else:
        stderr = exec_result.get("stderr", "unknown error")
        journal_entry += f"Script failed: {stderr[:200]}"
    if next_q:
        journal_entry += f"\n\n**Next**: {next_q}"
    memory.append_entry("journal.md", journal_entry)

    # Update agenda with next question
    agenda = _to_str(interp_result.get("agenda", ""))
    if agenda.strip():
        memory.write_file("agenda.md", agenda)


async def _run_investigate_cycle(
    client: httpx.AsyncClient,
    log,
    data_context: str,
    memory_context: str,
) -> dict:
    """Run a two-phase investigate cycle: generate script, execute, interpret."""
    from investigator import generate_investigation, interpret_results
    from sandbox import ensure_workspace, write_script, execute_script

    ensure_workspace()
    workspace_ctx = _build_workspace_context()

    # Phase 1: Generate script
    log.info("investigate.phase1", status="generating")
    gen_result = await generate_investigation(client, data_context, memory_context, workspace_ctx)

    script_code = gen_result.get("script_code", "")
    if not script_code.strip():
        log.warning("investigate.no_script", question=gen_result.get("question", ""))
        return {
            "gen": gen_result,
            "exec": {"success": False, "stdout": "", "stderr": "No script generated", "returncode": -1, "duration_seconds": 0},
            "interp": {"finding": "Failed to generate a script", "significance": "", "next_question": "", "should_save_tool": False, "agenda": ""},
        }

    # Write and execute
    try:
        script_path = write_script(
            gen_result.get("script_name", "investigation"),
            script_code,
            gen_result.get("description", ""),
        )
    except ValueError as e:
        log.warning("investigate.script_too_large", error=str(e))
        return {
            "gen": gen_result,
            "exec": {"success": False, "stdout": "", "stderr": str(e), "returncode": -1, "duration_seconds": 0},
            "interp": {"finding": f"Script rejected: {e}", "significance": "", "next_question": "", "should_save_tool": False, "agenda": ""},
        }

    log.info("investigate.phase2", status="executing", script=script_path.name)
    exec_result = execute_script(script_path)
    log.info("investigate.executed",
             success=exec_result["success"],
             duration=exec_result["duration_seconds"],
             stdout_len=len(exec_result["stdout"]),
             stderr_len=len(exec_result["stderr"]))

    # Phase 2: Interpret results
    log.info("investigate.phase3", status="interpreting")
    interp_result = await interpret_results(
        client,
        gen_result.get("question", ""),
        gen_result.get("script_name", ""),
        exec_result,
        memory_context,
    )

    # Handle tool saving if recommended
    if interp_result.get("should_save_tool") and exec_result["success"]:
        tool_name = interp_result.get("tool_name", gen_result.get("script_name", "tool"))
        from sandbox import TOOLS_DIR
        tool_path = TOOLS_DIR / f"{tool_name}.py"
        if not tool_path.exists():
            tool_path.write_text(script_path.read_text())
            log.info("investigate.tool_saved", name=tool_name)

    return {"gen": gen_result, "exec": exec_result, "interp": interp_result}


async def fetch_data(client: httpx.AsyncClient, log) -> tuple[dict | None, list[dict]]:
    """Fetch fresh data from Supabase."""
    log.info("cycle.fetch")
    timer = await get_current_timer(client)
    entries = await get_recent_entries(client, hours=48)
    return timer, entries


async def run_think_cycle(
    client: httpx.AsyncClient,
    log,
    cycle_count: int,
    cached_timer: dict | None,
    cached_entries: list[dict],
) -> None:
    """Execute one think cycle."""
    state = load_state()

    # --- Staleness detection ---
    current_fingerprint = _data_fingerprint(cached_timer, cached_entries)
    prev_fingerprint = state.get("data_fingerprint", "")
    if current_fingerprint == prev_fingerprint:
        unchanged = state.get("fingerprint_unchanged_cycles", 0) + 1
    else:
        unchanged = 0
    state["data_fingerprint"] = current_fingerprint
    state["fingerprint_unchanged_cycles"] = unchanged

    # 1. Determine mode
    scheduled_mode = _get_scheduled_mode(cycle_count)

    # Build a short context summary for mode selection
    data_context = _build_data_context(cached_timer, cached_entries, unchanged, cycle_count)
    context_summary = data_context[:500]

    # Let LLM override mode if it has reason to (but only sometimes to save compute)
    if cycle_count % 3 == 0:
        mode = await select_mode(client, scheduled_mode, context_summary)
    else:
        mode = scheduled_mode

    # --- Staleness override: divert stale modes when data hasn't changed ---
    stale_override = False
    if unchanged >= config.STALE_CYCLE_THRESHOLD and mode in ("observe", "hypothesize", "reflect", "plan"):
        # Rotate between productive stale-time modes
        stale_modes = ["investigate", "hypothesize", "critique", "investigate"]
        mode = stale_modes[unchanged % len(stale_modes)]
        stale_override = True

    log.info("cycle.think", mode=mode, cycle=cycle_count, scheduled=scheduled_mode,
             active_hours=_is_active_hours(), stale_cycles=unchanged,
             stale_override=stale_override)

    cycle_start = time.monotonic()

    try:
        # 2. Build context
        memory_context = _build_memory_context(mode, stale_cycles=unchanged)

        if mode == "investigate":
            # --- Two-phase investigate cycle ---
            think_start = time.monotonic()
            inv_result = await _run_investigate_cycle(client, log, data_context, memory_context)
            think_duration = round(time.monotonic() - think_start, 1)

            # Save to memory
            _save_investigation_to_memory(
                inv_result["gen"], inv_result["exec"], inv_result["interp"]
            )

            log.info("cycle.thought", mode=mode, think_seconds=think_duration,
                     question=inv_result["gen"].get("question", ""),
                     script_success=inv_result["exec"].get("success", False),
                     finding=_to_str(inv_result["interp"].get("finding", ""))[:200])
        else:
            # --- Standard single-phase think cycle ---
            think_start = time.monotonic()
            result = await think(
                client,
                mode=mode,
                context=data_context,
                memory_context=memory_context,
                stale_cycles=unchanged,
            )
            think_duration = round(time.monotonic() - think_start, 1)

            log.info("cycle.thought", mode=mode, think_seconds=think_duration,
                     **{k: v for k, v in result.items() if k != "message"})

            # Save to memory
            _save_thought_to_memory(mode, result)

            # Act if warranted (only observe mode during active hours)
            if result.get("should_act") and result.get("message") and _is_active_hours():
                sent = await send_message(result["message"])
                log.info("cycle.acted", sent=sent, message=result["message"])
                state["last_nudge_utc"] = datetime.now(timezone.utc).isoformat()

        # 6. Update state
        cycle_duration = round(time.monotonic() - cycle_start, 1)
        state["last_check_utc"] = datetime.now(timezone.utc).isoformat()
        state["last_think_mode"] = mode
        state["cycle_count"] = cycle_count

        state.setdefault("alert_history", []).append(
            {
                "time": state["last_check_utc"],
                "mode": mode,
                "should_act": False,
                "note": "",
            }
        )
        state["alert_history"] = state["alert_history"][-50:]

        save_state(state)
        log.info("cycle.complete", mode=mode, cycle_seconds=cycle_duration,
                 think_seconds=think_duration)

    except Exception as e:
        log.error("cycle.error", mode=mode, error=str(e), error_type=type(e).__name__)


async def main() -> None:
    """Main loop — think continuously with a minimum cooldown between cycles."""
    _setup_logging()
    log = structlog.get_logger()

    data_interval = config.CHECK_INTERVAL_SECONDS
    cooldown = config.THINK_COOLDOWN_SECONDS

    log.info(
        "coo.starting",
        data_interval=data_interval,
        cooldown=cooldown,
        model=config.OLLAMA_MODEL,
        think_enabled=config.OLLAMA_THINK,
        self_mod_enabled=config.SELF_MOD_ENABLED,
        num_ctx=config.OLLAMA_NUM_CTX,
        signal_enabled=config.SIGNAL_ENABLED,
        timezone=config.USER_TIMEZONE,
        active_hours=f"{config.ACTIVE_HOURS_START}-{config.ACTIVE_HOURS_END}",
    )

    # Ensure memory dir exists
    config.MEMORY_DIR.mkdir(parents=True, exist_ok=True)

    cached_timer = None
    cached_entries = []
    last_fetch = 0.0
    cycle_count = 0

    async with httpx.AsyncClient(timeout=httpx.Timeout(30.0, read=config.OLLAMA_READ_TIMEOUT)) as client:
        while True:
            # Fetch data if stale
            now = time.monotonic()
            if now - last_fetch >= data_interval or last_fetch == 0.0:
                try:
                    cached_timer, cached_entries = await fetch_data(client, log)
                    last_fetch = time.monotonic()
                except Exception as e:
                    log.error("fetch.error", error=str(e), error_type=type(e).__name__)

            # Run think cycle
            await run_think_cycle(client, log, cycle_count, cached_timer, cached_entries)
            cycle_count += 1

            # Brief cooldown to avoid hammering Ollama, then immediately think again
            log.info("coo.cooldown", seconds=cooldown)
            await asyncio.sleep(cooldown)


if __name__ == "__main__":
    asyncio.run(main())
