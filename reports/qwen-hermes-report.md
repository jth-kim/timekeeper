# Qwen-Hermes — Post-Mortem Report

**Run period**: 2026-03-08 22:01 AEDT to 2026-03-09 ~09:10 AEDT (~11 hours)
**Model**: qwen3:30b-a3b via Ollama (thinking enabled by default)
**Architecture**: NousResearch hermes-agent framework (cloned into container), custom Supabase tools registered via registry
**Total cycles**: 52 completed, 1 error (2%)

---

## What Was Built

The hermes-agent framework was cloned into a container and driven programmatically via `AIAgent.run_conversation()`. The driver registered 4 custom tools (`get_current_timer`, `get_recent_entries`, `get_alert_thresholds`, `send_nudge`) and wrote a SOUL.md containing the COO identity, system prompt, and alert thresholds. Hermes's own memory system (MEMORY.md, session DB, context compression) was used instead of the custom markdown memory files.

---

## What Went Wrong

### The experiment was fundamentally misconfigured

Two critical integration failures meant hermes was running blind:

**1. Tools never reached the agent.**
Custom tools were registered via `tools.registry.register()` with toolset `"timekeeper"`, but hermes resolves tools through `model_tools.get_tool_definitions()` which filters by known toolsets defined in `toolsets.py`. The `"timekeeper"` toolset was never declared there. Result: hermes had 10 generic tools (memory, session_search, execute_code, etc.) but **zero data access tools**. It could not check the timer or query time entries.

**2. SOUL.md was written to the wrong path.**
The driver wrote SOUL.md to `$HERMES_HOME/SOUL.md` (`/data/hermes/SOUL.md`). But hermes's `prompt_builder.build_context_files_prompt()` looks for SOUL.md in CWD (`/app/`) then `~/.hermes/` — it does not check `HERMES_HOME`. Result: hermes ran with its default identity ("You are Hermes Agent, an intelligent AI assistant created by Nous Research"). The COO persona, structured thinking framework, and alert thresholds were never injected.

### The agent's behaviour was rational given its configuration

Hermes received cycle trigger messages saying "Use your tools to check the current timer and recent time entries" but had no tools to do so. With no data tools, no domain identity, and no cognitive framework, it did the only thing available: used its `memory` tool to log timestamps.

---

## What Hermes Actually Did

### MEMORY.md (3.6KB)

18 entries, all timestamped cycle logs:

> "COO Cycle 0 started at Sunday, 22:13 AEDT (UTC+11, 2026-03-08T11:13Z). Current session posture: ACTIVE HOURS — user likely working."

Zero observations about user behaviour. Zero mentions of STAR, SEIFUKU, BBOY, or BOJ.

### Session structure

3 session files (617KB total). Two false starts, then one 553KB session carrying all 52 cycles as a single growing conversation (200 messages). No session rotation or summarisation. Cycle times degraded from ~2 minutes to ~13 minutes as context grew.

### Behavioural loop

Every cycle for 11 hours:
1. Read MEMORY.md
2. Write a timestamp entry
3. Report "No further action required"

Around cycle 17, noticed memory at 85% capacity. Consolidated timestamps into a range summary. Then continued filling with timestamps.

---

## What We Can Still Learn

### Hermes's framework stability is real

1 error in 52 cycles. The framework handled the model's degenerate output gracefully — no crashes, no state corruption, no runaway resource consumption. Container ran stable for the full 11 hours.

### Memory management works but is content-agnostic

Hermes's character-limited MEMORY.md and compression system functioned correctly. The problem is that it compresses and manages whatever the agent writes — if the agent writes garbage, you get well-managed garbage.

### The model needs structure imposed, not offered

Given total freedom to decide what to do each cycle, qwen3:30b-a3b chose to do nothing. The custom architecture's mode rotation (forcing observe → reflect → act) prevents this failure mode. The hermes framework assumes a model capable of self-directed initiative — this model isn't, at least not without strong identity anchoring.

### Integration with hermes requires understanding its discovery paths

- Tools must be in a declared toolset in `toolsets.py`, or added to `_LEGACY_TOOLSET_MAP`, or injected via `enabled_toolsets` parameter
- SOUL.md must be in CWD or `~/.hermes/`, not `HERMES_HOME`
- The `skip_context_files=False` flag was correctly set but pointless since the file wasn't findable

---

## Verdict

**Experiment invalid.** The comparison was "hermes with no data access and no identity" vs "custom architecture with full data access and full identity." No conclusions about hermes's architectural merits can be drawn. A rerun with correct tool registration and SOUL.md placement is needed.

---

## Rerun readiness (epoch 2)

The next root-level `qwen-hermes` experiments are configured to address the above:

1. Write `SOUL.md` to `/app/SOUL.md` and `~/.hermes/SOUL.md` (plus `/data/hermes/SOUL.md` backup)
2. Register timekeeper tools and inject a `timekeeper` legacy toolset mapping
3. Start `AIAgent` with explicit `enabled_toolsets` including `timekeeper`
4. Gate self-modification via `SELF_MOD_ENABLED` and experiment-local config mounts
