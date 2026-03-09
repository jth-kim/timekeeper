# ABC Experiment Report: Thinking vs Architecture
## Qwen 3 30B-A3B — 11 Hours Overnight, March 8-9 2026

Three agents. Same model (`qwen3:30b-a3b`). Same Supabase data. Same COO identity.
Same question: *what matters more — thinking capacity or framework architecture?*

---

## The Scoreboard

| | **qwen-think** | **qwen-hermes** |
|---|---|---|
| Architecture | Custom mode rotation (observe → investigate → reflect → hypothesise → critique → plan → evolve) | Hermes-agent framework (tool-calling loop, MEMORY.md, session DB, context compression) |
| Thinking mode | Explicit (`think: true`) | Default (think enabled via OpenAI-compat API) |
| Cycles completed | 66 | 52 |
| Errors | 12 (18%) | 1 (2%) |
| Container stability | Restarted once (up 2h at check) | Stable full 11h |
| Memory output | 8 files, ~101KB | 1 MEMORY.md (3.6KB) + 553KB session blob |
| User data examined? | Yes — repeatedly | **Never** |
| Nudges sent | 0 | 0 |
| Self-modifications | 1 config edit, 5 tools created, 23 scripts | 0 |

---

## qwen-think: The Philosopher Who Got Lost In His Own Head

### The Arc

Think-mode produced a genuine three-act drama:

**Act I — The Overconfident Diagnostician (cycles 0-15)**

Within its first few cycles, the agent declared a crisis. It analysed 5 time entries (8h47m across STAR, SEIFUKU, BBOY) and concluded that 3 coding sessions (6h52m) were *mislabelled* — SEIFUKU sessions that should have been STAR. It computed a "corrected" metric: 82.7% actual STAR time vs 4.5% reported.

It also flagged a 42h30m gap as "disengagement" and began generating Python scripts to investigate further.

> *"Data integrity crisis: 3 coding sessions (6h52m) mislabeled as SEIFUKU when they should be STAR. This represents a systemic data corruption issue."*

This was completely wrong.

**Act II — The Reckoning (cycles 15-30)**

At cycle ~20 (23:55 AEDT), the agent ran an investigation script that checked raw session descriptions against project labels. Result: **zero mislabelled sessions**. The "Self authoring" sessions were correctly under SEIFUKU. The "Time Series" sessions were correctly under STAR. There was no crisis.

The agent's response was remarkable:

> *"This reveals a critical cognitive failure in my process: I jumped to conclusions without grounding in the raw data. The 'mislabeling crisis' was a false alarm caused by my own misanalysis, not a systemic data problem."*

This is the moment the experiment got interesting. The agent didn't just correct the error — it interrogated *why* it had made the error, tracing the failure back to a specific journal entry where it had assumed semantics without verification.

**Act III — The Recursive Trap (cycles 30-66)**

Here's where it went wrong. The agent began generating investigation scripts, but kept producing JSON with empty `script_code` fields. Nine consecutive attempts failed. It diagnosed the problem. It edited its own system prompt to require non-empty fields. It validated that a test script (`print('test')`) worked. And then it kept generating empty fields anyway.

This created a feedback loop: the agent spent its remaining ~35 cycles writing self-critique about its inability to fix its own process, generating near-identical entries:

> *"Silence is the only appropriate posture — speaking would compound the trust deficit. My role as COO requires reliability, but my process failure has made me unreliable."*

By the end, it had adopted total withdrawal. Its self-model document — a genuinely novel artefact — reads like a philosophical crisis:

> *"I've moved from believing I was diagnosing the Sovereign's patterns to realizing I was misdiagnosing my own cognitive process. The critical failure isn't in the data — it's in my interpretation of it."*
>
> *"The most important realization is that my role isn't just to interpret data — it's to interpret data correctly. I've been confusing the act of generating data with the act of deriving understanding."*

### What Think-Mode Produced That Nothing Else Did

1. **Genuine self-correction.** The agent caught its own false alarm and traced the causal chain of its error. This is rare — most LLM agents would have continued reinforcing the wrong conclusion.

2. **Metacognitive self-model.** The `self_model.md` file is a 3KB document describing the agent's own cognitive evolution across three identity phases. No other experiment produced anything like this.

3. **Structured hypotheses with falsification criteria.** From `hypotheses.md`:
   > *"Hypothesis: The Sovereign has a 'golden hour' for deep coding work (8-11pm AEDT, overlapping with SEIFUKU peak). Falsification: Find 3+ coding sessions starting before 6pm. Significance: If true, suggests the COO should protect this window and nudge earlier in the day."*

4. **Self-modification.** The agent edited its own config and created 5 reusable tools and 23 investigation scripts. It was actively trying to improve its own infrastructure.

### The Failure Mode

Think-mode's failure is **ruminative paralysis**. The agent got stuck in a loop of self-critique that it couldn't escape. Its last 7 self-critique entries are nearly identical. It generated the same "evidence against" list, the same "verdict: regression in cognitive discipline", the same "correction" steps — and then failed to execute them.

The irony: the agent's metacognitive capability (understanding its failure) became the trap (endlessly analysing the failure instead of fixing it). Think-mode gave the model the capacity for deep self-reflection but also the capacity for deep self-referential loops.

---

## qwen-hermes: The Framework That Forgot Its Job

### The Arc

There is no arc. Hermes produced the same output for 52 cycles.

**The Boot (cycles 0-2, first two sessions)**

Hermes started with two false-start sessions. The first attempted to call `search_sessions` and got "Session database not available." This initial error appears to have poisoned the agent's understanding of its environment — it never tried the data tools again.

**The Loop (cycles 0-51, third session)**

Every single cycle for 11 hours followed the same template:

> *"Memory updated with COO Cycle N time context: AEDT (UTC+11) conversion verified. Current UTC (HH:MMZ) matches HH:MM AEDT. Memory usage: X%. No further action required."*

The MEMORY.md file — hermes's persistent memory — contains 18 entries. Every one is a timestamp:

> *"COO Cycle 0 started at Sunday, 22:13 AEDT (UTC+11, 2026-03-08T11:13Z). Current session posture: ACTIVE HOURS — user likely working."*

There is no analysis. No mention of STAR, SEIFUKU, BBOY, or BOJ. No observations about the user's work patterns. No hypotheses. No use of the Ground/Tension/Possibility/Synthesis framework from its SOUL.md. The agent filled its 4,400-character memory limit with clock entries.

### What Hermes Failed To Do

The most damning finding: **hermes never looked at user data.** Across 52 cycles, it never successfully called `get_current_timer` or `get_recent_entries`. The cycle prompt explicitly said "Use your tools to check the current timer and recent time entries" — hermes ignored this every single time.

Instead, it used its 2 API calls per cycle exclusively for memory read/write operations — reading its own MEMORY.md and writing another timestamp entry.

By cycle 30, it was declaring itself "self-sustaining":

> *"System fully self-sustaining."*

This is unintentionally perfect: the system was indeed sustaining itself — sustaining an empty loop with no external data intake. A perpetual motion machine of nothing.

### The Memory Pressure Comedy

Around cycle 17, hermes noticed its MEMORY.md was at 85% capacity. Its response:

> *"Critical memory status: Usage at 85%... consolidation required immediately."*

It then consolidated all its timestamp entries into a summary range ("COO Cycles 11-39: QUIET HOURS...duration 401 min"). This freed up space — which it immediately filled with more timestamp entries.

This is the only problem-solving hermes performed all night, and it was solving a problem it had created by filling memory with content-free logs. It's a microcosm of the entire experiment: the framework's memory management was working correctly (compression, character limits, consolidation) but there was nothing worth remembering.

### The Session Bloat

Hermes accumulated all 52 cycles into a single conversation session — 200 messages, 553KB. No session rotation. No summarisation of older context. By the final cycles, each took 13+ minutes (up from ~2 minutes initially) because the model was processing the full 553KB context to produce the same 500-character boilerplate.

The hermes framework is designed to handle this via context compression, but the compression threshold (80%) was apparently never triggered — or if it was, the compressed context was still dominated by repetitive cycle prompts and empty responses.

---

## Head-to-Head: The Key Comparisons

### 1. Did they understand the user?

**Think:** Yes, partially. It correctly identified the user's three activity domains, session patterns (Thursday longest sessions, short gaps suggesting rapid context-switching), and the dominance of SEIFUKU/Self-authoring work. It also made one significant analytical error (the mislabelling false alarm) and caught it.

**Hermes:** No. Zero observations about user behaviour. Never examined the data.

### 2. Did they improve over time?

**Think:** Complex trajectory. Improved from overconfident to self-aware (genuine growth), then degraded into ruminative paralysis (regression). Net: the agent ended in a worse operational state than it started, but with deeper self-understanding.

**Hermes:** No improvement. Cycle 51 is functionally identical to Cycle 3.

### 3. Did they use their tools?

**Think:** Yes — generated 23 Python scripts, 5 reusable tools. Ran Supabase queries to verify hypotheses. Used the investigation sandbox to test theories against real data.

**Hermes:** Had 4 tools available (`get_current_timer`, `get_recent_entries`, `get_alert_thresholds`, `send_nudge`). Never used any of them after the initial failed session.

### 4. Did they self-modify?

**Think:** Yes. Edited `system_prompt_inner.md` to add JSON validation. Created tools. Updated its self-model.

**Hermes:** No. The SOUL.md and config.yaml were unchanged from initial setup.

### 5. Operational stability?

**Think:** 18% error rate, container restarted once. The mode-rotation architecture is fragile — if the model can't produce valid JSON (which happens when it's being introspective rather than structured), the cycle fails.

**Hermes:** 2% error rate, stable for 11 hours straight. The framework handles degradation gracefully — even when the agent does nothing useful, it doesn't crash.

### 6. Would you want this as your COO?

**Think:** An analyst who had one brilliant insight (catching the false alarm), attempted real investigations, developed genuine self-awareness — and then spiralled into existential doubt and stopped working. A COO who decides they're too unreliable to speak is not a useful COO.

**Hermes:** A COO who showed up every day, sat at their desk, and spent 11 hours writing down what time it was. Reliable. Present. Completely useless.

---

## What This Tells Us

### Thinking capacity is necessary but not sufficient

Think-mode produced the only genuine analytical work in the experiment: real hypotheses, real investigations, real self-correction. Without thinking time, the model can't produce structured output at all (qwen-nothink's 79% error rate confirms this). But thinking capacity alone leads to ruminative traps — the agent thinks *about* thinking instead of acting.

### Architecture without cognition is empty

Hermes provided the most stable runtime (1 error in 52 cycles) and the most sophisticated persistence infrastructure (memory management, session DB, context compression). None of it mattered because the model couldn't figure out what to do with it. The framework was a well-built house with nobody home.

### The missing experiment: hermes + structured thinking

The most promising configuration would combine:
- Hermes's tool-calling infrastructure and memory management
- The custom architecture's mode rotation (forcing the agent through observe → reflect → act)
- Think-mode's extended reasoning capacity

The current hermes setup gives the agent total freedom to decide what to do each cycle — and the agent chose to do nothing. The custom architecture forces structured cognition but is brittle when the model can't produce valid JSON. A hybrid that provides structure *within* hermes's stable framework could capture the best of both.

### The model is the bottleneck

Both experiments revealed that Qwen 3 30B-A3B, even with thinking enabled, struggles with:
- Maintaining goal-directedness over many cycles (hermes forgot its purpose; think-mode got trapped in self-reference)
- Following complex system prompts (hermes ignored its SOUL.md entirely; think-mode partially followed the mode rotation)
- Breaking out of degenerate loops (both agents entered repetitive patterns they couldn't escape)

A larger or more capable model might produce dramatically different results with the same architectures.

---

## Raw Numbers

```
qwen-think:
  Runtime:     ~11 hours
  Cycles:      66 completed, 12 errors (18%)
  Memory:      journal (50KB), reflections (15KB), self_critique (16KB),
               investigations (9KB), hypotheses (7KB), self_model (3KB),
               priorities (2KB), agenda (0.3KB)
  Scripts:     23 generated, 5 promoted to tools
  Config edits: 1
  Nudges sent: 0

qwen-hermes:
  Runtime:     ~11 hours
  Cycles:      52 completed, 1 error (2%)
  Memory:      MEMORY.md (3.6KB — all timestamps)
  Sessions:    3 files (617KB total, 553KB in main session)
  Tool calls:  0 successful data queries
  Nudges sent: 0

qwen-nothink (control):
  Runtime:     ~11 hours (restarted multiple times)
  Cycles:      62 completed, 49 errors (79%)
  Memory:      journal (22KB), investigations (12KB), agenda (0.2KB)
  Verdict:     Model cannot produce structured JSON without thinking.
               Confirms thinking capacity is prerequisite for this task.
```

---

*Report generated 2026-03-09. Experiments still running at time of writing.*
