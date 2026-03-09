"""
Timekeeper COO — Hermes Agent Driver

Uses the actual hermes-agent framework (cloned into /app/hermes-agent).
Registers custom Supabase tools via hermes's tool registry, then drives
AIAgent in a periodic loop. Hermes handles its own memory, context
compression, and tool-calling loop.
"""

import asyncio
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import structlog

# --- Environment setup (must happen before hermes imports) ---

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://host.containers.internal:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "qwen3:30b-a3b")
HERMES_HOME = os.environ.get("HERMES_HOME", "/data/hermes")
COOLDOWN = int(os.environ.get("THINK_COOLDOWN_SECONDS", "120"))
USER_TIMEZONE = os.environ.get("USER_TIMEZONE", "Australia/Sydney")
ACTIVE_HOURS_START = int(os.environ.get("ACTIVE_HOURS_START", "6"))
ACTIVE_HOURS_END = int(os.environ.get("ACTIVE_HOURS_END", "23"))
LOG_DIR = Path(os.environ.get("LOG_DIR", "/data/logs"))
CONFIG_DIR = Path(os.environ.get("CONFIG_DIR", "/data/config"))
SIGNAL_ENABLED = os.environ.get("SIGNAL_ENABLED", "false").lower() == "true"
SELF_MOD_ENABLED = os.environ.get("SELF_MOD_ENABLED", "true").lower() == "true"

# Set hermes home directory
os.environ["HERMES_HOME"] = HERMES_HOME
# Ensure OpenAI-compatible endpoint is configured
os.environ["OPENAI_BASE_URL"] = f"{OLLAMA_BASE_URL}/v1"
os.environ.setdefault("OPENAI_API_KEY", "ollama")

# Create hermes directories
for d in ["memories", "sessions", "skills"]:
    Path(HERMES_HOME, d).mkdir(parents=True, exist_ok=True)

# Write hermes config
_hermes_config = Path(HERMES_HOME) / "config.yaml"
if not _hermes_config.exists():
    import yaml
    config_data = {
        "model": {
            "default": OLLAMA_MODEL,
            "provider": "custom",
            "base_url": f"{OLLAMA_BASE_URL}/v1",
        },
        "memory": {
            "memory_enabled": True,
            "user_profile_enabled": True,
            "memory_char_limit": 4400,
            "user_char_limit": 2200,
            "nudge_interval": 6,
            "flush_min_turns": 3,
        },
        "compression": {
            "enabled": True,
            "threshold": 0.80,
        },
        "agent": {
            "max_turns": 30,
        },
    }
    _hermes_config.write_text(yaml.dump(config_data, default_flow_style=False))


# --- Write SOUL.md (COO identity for hermes) ---

def _write_soul():
    """Write the COO identity as hermes SOUL.md."""
    # Compose from our config files
    parts = []
    identity_path = CONFIG_DIR / "coo_identity.md"
    if identity_path.exists():
        parts.append(identity_path.read_text())
    prompt_path = CONFIG_DIR / "system_prompt.md"
    if prompt_path.exists():
        parts.append(prompt_path.read_text())
    inner_path = CONFIG_DIR / "system_prompt_inner.md"
    if inner_path.exists():
        parts.append(inner_path.read_text())

    # Load thresholds
    thresholds_path = CONFIG_DIR / "thresholds.toml"
    if thresholds_path.exists():
        import tomli
        with open(thresholds_path, "rb") as f:
            thresholds = tomli.load(f)
        parts.append(f"## Alert Thresholds\n\n```json\n{json.dumps(thresholds, indent=2)}\n```")

    parts.append(
        "## Runtime Constraints\n\n"
        f"- SELF_MOD_ENABLED: {str(SELF_MOD_ENABLED).lower()}\n"
        "- If self-modification is disabled, do not attempt config edits.\n"
        "- Always prioritize tool-grounded observation over introspection."
    )
    soul_text = "\n\n---\n\n".join(parts)

    # Hermes discovers SOUL.md from cwd (/app) and ~/.hermes; write both.
    soul_targets = [
        Path("/app/SOUL.md"),
        Path.home() / ".hermes" / "SOUL.md",
        Path(HERMES_HOME) / "SOUL.md",  # backup copy for debugging
    ]
    for soul_path in soul_targets:
        soul_path.parent.mkdir(parents=True, exist_ok=True)
        soul_path.write_text(soul_text)

_write_soul()


# --- Register custom Supabase tools with hermes registry ---

def _register_tools() -> list[str]:
    """Register COO-specific tools with hermes's tool registry.

    We import the registry module directly (bypassing tools/__init__.py)
    because hermes's __init__ eagerly imports all tool modules, many of
    which have heavy optional deps (firecrawl, fal, etc.) we don't need.
    """
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "tools.registry",
        "/app/hermes-agent/tools/registry.py",
    )
    registry_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(registry_mod)
    registry = registry_mod.registry

    import httpx as _httpx
    from datetime import timedelta

    def _supabase_headers():
        return {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
        }

    def get_current_timer_handler(args, **kwargs):
        """Get the currently running time-tracking timer."""
        headers = {**_supabase_headers(), "Accept-Profile": "live"}
        resp = _httpx.get(
            f"{SUPABASE_URL}/rest/v1/current_timer_state",
            headers=headers,
            params={"state_key": "eq.primary", "select": "*"},
            timeout=30.0,
        )
        resp.raise_for_status()
        rows = resp.json()
        if rows:
            return json.dumps(rows[0], default=str)
        return json.dumps({"status": "No timer currently running"})

    def get_recent_entries_handler(args, **kwargs):
        """Get recent completed time entries."""
        hours = args.get("hours", 48)
        limit = args.get("limit", 100)
        since = (datetime.now(timezone.utc) - timedelta(hours=hours)).isoformat()
        resp = _httpx.get(
            f"{SUPABASE_URL}/rest/v1/time_entries",
            headers=_supabase_headers(),
            params={
                "select": "start,stop,duration,client_name,project_name,tags,description",
                "start": f"gte.{since}",
                "order": "start.desc",
                "limit": str(limit),
            },
            timeout=30.0,
        )
        resp.raise_for_status()
        entries = resp.json()
        return json.dumps({
            "count": len(entries),
            "hours_queried": hours,
            "entries": entries,
        }, default=str)

    def get_alert_thresholds_handler(args, **kwargs):
        """Get alert threshold configuration."""
        thresholds_path = CONFIG_DIR / "thresholds.toml"
        if thresholds_path.exists():
            import tomli
            with open(thresholds_path, "rb") as f:
                return json.dumps(tomli.load(f))
        return json.dumps({"error": "No thresholds config found"})

    def send_nudge_handler(args, **kwargs):
        """Send a nudge to the Sovereign."""
        message = args.get("message", "")
        if not SIGNAL_ENABLED:
            return json.dumps({"sent": False, "message": message, "note": "Signal disabled, logged only"})
        return json.dumps({"sent": False, "message": message, "note": "Signal not implemented"})

    timekeeper_tools: list[str] = []

    # Register tools
    registry.register(
        name="get_current_timer",
        toolset="timekeeper",
        schema={
            "name": "get_current_timer",
            "description": "Get the currently running time-tracking timer. Returns client, project, description, tags, start time, and elapsed time if a timer is active.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
        handler=get_current_timer_handler,
    )
    timekeeper_tools.append("get_current_timer")

    registry.register(
        name="get_recent_entries",
        toolset="timekeeper",
        schema={
            "name": "get_recent_entries",
            "description": "Get recent completed time entries. Each entry has: start, stop, duration (ISO format like PT1H30M), client_name, project_name, tags, description. Identity-level clients: STAR (knowledge work), BBOY (physical), SEIFUKU (admin), BOJ (finance).",
            "parameters": {
                "type": "object",
                "properties": {
                    "hours": {"type": "integer", "description": "Hours back to query (default 48)", "default": 48},
                    "limit": {"type": "integer", "description": "Max entries (default 100)", "default": 100},
                },
                "required": [],
            },
        },
        handler=get_recent_entries_handler,
    )
    timekeeper_tools.append("get_recent_entries")

    registry.register(
        name="get_alert_thresholds",
        toolset="timekeeper",
        schema={
            "name": "get_alert_thresholds",
            "description": "Get alert threshold config: goal neglect days per client, allocation targets, anomaly z-scores, nudge cadence limits.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
        handler=get_alert_thresholds_handler,
    )
    timekeeper_tools.append("get_alert_thresholds")

    registry.register(
        name="send_nudge",
        toolset="timekeeper",
        schema={
            "name": "send_nudge",
            "description": "Send a message/nudge to the Sovereign (user) via Signal. Only when you have something specific and actionable. Most cycles, stay silent.",
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {"type": "string", "description": "Short, direct, warm message."},
                },
                "required": ["message"],
            },
        },
        handler=send_nudge_handler,
    )
    timekeeper_tools.append("send_nudge")

    if SELF_MOD_ENABLED:
        def edit_coo_config_handler(args, **kwargs):
            """Edit a COO config file when self-mod is enabled."""
            file_name = args.get("file", "")
            content = args.get("content", "")
            allowed = {"coo_identity.md", "system_prompt_inner.md"}
            if file_name not in allowed:
                return json.dumps({"ok": False, "error": f"file not allowed: {file_name}"})
            path = CONFIG_DIR / file_name
            try:
                backup = CONFIG_DIR / f"{file_name}.bak"
                if path.exists():
                    backup.write_text(path.read_text())
                path.write_text(content)
                return json.dumps({"ok": True, "file": file_name})
            except Exception as e:
                return json.dumps({"ok": False, "error": str(e)})

        registry.register(
            name="edit_coo_config",
            toolset="timekeeper",
            schema={
                "name": "edit_coo_config",
                "description": "Edit COO config file content (coo_identity.md or system_prompt_inner.md). Use sparingly and only with clear reason.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file": {"type": "string", "description": "Target file: coo_identity.md or system_prompt_inner.md"},
                        "content": {"type": "string", "description": "Full replacement file content"},
                    },
                    "required": ["file", "content"],
                },
            },
            handler=edit_coo_config_handler,
        )
        timekeeper_tools.append("edit_coo_config")

    # Hermes toolset resolution requires named toolsets. Inject our custom set.
    try:
        import model_tools
        legacy_map = getattr(model_tools, "_LEGACY_TOOLSET_MAP", None)
        if isinstance(legacy_map, dict):
            legacy_map["timekeeper"] = timekeeper_tools
    except Exception:
        pass

    return timekeeper_tools


# Register tools before importing AIAgent (it reads the registry at init)
TIMEKEEPER_TOOL_NAMES = _register_tools()

# Now import hermes AIAgent
from run_agent import AIAgent


# --- Logging ---

def _local_timestamper(logger, method, event_dict):
    try:
        tz = ZoneInfo(USER_TIMEZONE)
    except Exception:
        tz = timezone.utc
    event_dict["timestamp"] = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S %Z")
    return event_dict


def _setup_logging():
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_file = open(LOG_DIR / "coo.jsonl", "a")
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
    try:
        tz = ZoneInfo(USER_TIMEZONE)
    except Exception:
        tz = timezone.utc
    local_hour = datetime.now(tz).hour
    return ACTIVE_HOURS_START <= local_hour < ACTIVE_HOURS_END


def _local_time_str() -> str:
    try:
        tz = ZoneInfo(USER_TIMEZONE)
    except Exception:
        tz = timezone.utc
    return datetime.now(tz).strftime("%A %H:%M %Z")


# --- Main loop ---

def main():
    _setup_logging()
    log = structlog.get_logger()

    log.info(
        "coo.starting",
        architecture="hermes-agent",
        model=OLLAMA_MODEL,
        hermes_home=HERMES_HOME,
        self_mod_enabled=SELF_MOD_ENABLED,
        timekeeper_tools=TIMEKEEPER_TOOL_NAMES,
        cooldown=COOLDOWN,
        signal_enabled=SIGNAL_ENABLED,
        timezone=USER_TIMEZONE,
        active_hours=f"{ACTIVE_HOURS_START}-{ACTIVE_HOURS_END}",
    )

    # Create the hermes agent — pointed at Ollama, with our custom tools
    agent = AIAgent(
        base_url=f"{OLLAMA_BASE_URL}/v1",
        api_key="ollama",
        model=OLLAMA_MODEL,
        max_iterations=15,
        quiet_mode=True,
        skip_context_files=False,  # Load SOUL.md from /app and ~/.hermes
        skip_memory=False,         # Let hermes manage MEMORY.md / USER.md
        enabled_toolsets=["timekeeper", "memory", "session_search"],
        platform="api",
    )

    log.info("coo.agent_created", model=OLLAMA_MODEL)

    # Conversation history carried across cycles
    conversation_history = []
    cycle_count = 0

    while True:
        now_utc = datetime.now(timezone.utc)
        local_time = _local_time_str()
        active = _is_active_hours()

        # Build cycle trigger message
        cycle_msg = (
            f"## COO Cycle {cycle_count} — {local_time}\n\n"
            f"Current time (UTC): {now_utc.isoformat()}\n"
            f"Local time: {local_time}\n"
            f"Day: {now_utc.strftime('%A')}\n"
            f"Posture: {'ACTIVE HOURS — user may be working' if active else 'QUIET HOURS — deep thinking time.'}\n\n"
            f"Use your tools to check the current timer and recent time entries. "
            f"Think carefully about what you observe. Update your memory with insights. "
            f"Only send a nudge if you have something specific to say."
            f"{' Self-modification is disabled in this run; do not attempt config edits.' if not SELF_MOD_ENABLED else ''}"
        )

        log.info("cycle.start", cycle=cycle_count, active_hours=active)
        cycle_start = time.monotonic()

        try:
            result = agent.run_conversation(
                user_message=cycle_msg,
                conversation_history=conversation_history,
            )

            cycle_duration = round(time.monotonic() - cycle_start, 1)

            if result is None:
                log.warning("cycle.null_result", cycle=cycle_count,
                            cycle_seconds=cycle_duration)
                cycle_count += 1
                log.info("coo.cooldown", seconds=COOLDOWN)
                time.sleep(COOLDOWN)
                continue

            # Update conversation history for next cycle
            messages = result.get("messages")
            if messages is not None:
                conversation_history = messages
            final_response = result.get("final_response") or ""
            api_calls = result.get("api_calls", 0)

            log.info(
                "cycle.complete",
                cycle=cycle_count,
                cycle_seconds=cycle_duration,
                api_calls=api_calls,
                response_len=len(final_response),
                history_len=len(conversation_history),
                completed=result.get("completed", False),
            )

            # Log the response content
            if final_response:
                log.info("cycle.response", content=final_response[:1000])

        except Exception as e:
            cycle_duration = round(time.monotonic() - cycle_start, 1)
            log.error("cycle.error", error=str(e), error_type=type(e).__name__,
                      cycle_seconds=cycle_duration)

        cycle_count += 1
        log.info("coo.cooldown", seconds=COOLDOWN)
        time.sleep(COOLDOWN)


if __name__ == "__main__":
    main()
