# Hermes Agent Strategy — Architecture Comparison

## What is Hermes Agent?

[hermes-agent](https://github.com/NousResearch/hermes-agent) is Nous Research's open-source "self-improving AI agent" framework. It is model-agnostic — it wraps any OpenAI-compatible API (including Ollama) in a tool-calling agent loop with built-in persistence. It is not a model; it is an architecture for persistent agency.

## Why test it?

The core problem in the COO system is **persistence** — maintaining coherent state, memory, and identity across an indefinite number of reasoning cycles. Our custom architecture (naive-coo, qwen-think, qwen-nothink) solves this with hand-built markdown memory files, mode rotation schedules, manual context assembly, and entry caps.

Hermes solves the same problem differently, and its approach is worth benchmarking against ours.

## Hermes persistence architecture

### Layer 1: Markdown memory files
- `MEMORY.md` — agent's personal notes: environment facts, learned solutions, tool quirks.
- `USER.md` — user profile: name, role, preferences, communication style.
- Character-limited (~2,200 / ~1,375 chars), entry-delimited.
- Frozen snapshot at session start, injected into system prompt. Mid-session writes update disk but not the live prompt (preserves prefix cache efficiency).
- Scanned for prompt injection before acceptance.

### Layer 2: SQLite session database
- Full conversation history per session (messages, tool calls, timestamps).
- FTS5 full-text search across past sessions.
- Session resume support.
- Parent-child session tracking (for compression-triggered splits).

### Layer 3: Context compression
- When token usage hits ~85% of model context, compresses mid-conversation.
- Algorithm: protect first N + last N turns, summarize everything between.
- Uses an auxiliary model for summarization (falls back to primary model).
- Sanitizes orphaned tool_call/tool_result pairs after compression.

### Layer 4: Skills (procedural memory)
- Learned procedures stored as `SKILL.md` files.
- Created from experience, improved during use.
- Invoked as slash commands, injected as structured messages.

## How our custom architecture differs

| Aspect | Custom COO | Hermes |
|---|---|---|
| Memory | Multiple markdown files (journal, reflections, priorities, hypotheses, self-model, agenda, investigations, self-critique) with per-file entry caps | Two markdown files (MEMORY.md, USER.md) with character limits |
| Context management | Manual assembly per mode — different memory subsets injected based on thinking mode | Automatic — frozen snapshot at session start, context compression when approaching limits |
| Thinking structure | Explicit mode rotation (observe, reflect, plan, critique, hypothesize, evolve, investigate) with structured JSON schemas per mode | Free-form — agent decides what to think about based on tools and conversation flow |
| Persistence | Markdown files only, no session search, no compression | SQLite + markdown + FTS5 search + context compression |
| Tool use | Investigation sandbox (write & execute Python scripts) | OpenAI function-calling based tools, plus terminal execution |
| Self-improvement | Evolve mode can edit own config files | Skills system creates reusable procedures from experience |

## What we're testing

**Same model** (qwen3:30b-a3b), **same data** (Supabase time entries), **same identity** (COO role), **different architecture**.

The question: does hermes's persistence mechanism — particularly context compression, session search, and the tool-calling loop — produce qualitatively different COO behavior than our hand-crafted mode rotation and structured thinking?

### Specific things to compare

1. **Memory quality**: Does hermes's compressed memory retain the right information? Does our explicit structure force better thinking?
2. **Initiative**: Does hermes's free-form approach produce more or less agency than our mode rotation?
3. **Self-improvement**: Does hermes's skills system lead to genuine operational improvements, or does our evolve mode do better?
4. **Degradation**: As cycles accumulate, which architecture degrades more gracefully?
5. **Tool calling**: How well does qwen3:30b-a3b handle OpenAI-format function calling via Ollama? This is a key risk.

## Implementation

The qwen-hermes experiment installs hermes-agent and drives it programmatically via a periodic loop. Instead of our custom context assembly and mode rotation, hermes manages its own memory, context, and reasoning strategy. We provide it with:

- COO identity and role (via hermes config / system prompt)
- Custom tools for Supabase data access (in OpenAI function-calling format)
- Alert thresholds (via tool or config)
- Signal output stub (same as other experiments)

The driver loop:
1. Periodically sends a "cycle trigger" message with current data context
2. Lets hermes process it (tool calls, memory updates, reasoning)
3. Logs the response
4. Handles any nudge actions
5. Sleeps for cooldown

Hermes handles everything else: memory persistence, context compression, session state.
