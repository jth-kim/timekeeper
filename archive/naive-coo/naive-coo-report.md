# Naive COO — Post-Mortem Report

**Run period**: ~2026-03-03 to 2026-03-08 (approx. 5 days)
**Model**: llama3.3:70b via Ollama
**Total cycles logged**: ~149+ (session count, not lifetime — container restarted several times during development)
**Architecture**: Containerised Python loop (Podman), markdown-based memory, sandboxed Python investigation scripts

---

## What Was Built

A continuously-running LLM agent ("COO") that monitors Toggl time-tracking data via Supabase and maintains a persistent identity across cycles. The agent cycles through 7 thinking modes on a schedule:

- **observe** — read current data, form an opinion
- **reflect** — deeper pattern analysis
- **plan** — update working priorities
- **critique** — self-examination
- **hypothesize** — form/evaluate falsifiable predictions
- **investigate** — write and execute Python scripts against live data
- **evolve** — update self-model and optionally edit own config

Memory was persisted across cycles via markdown files:
`journal.md`, `reflections.md`, `priorities.md`, `self_critique.md`, `hypotheses.md`, `investigations.md`, `agenda.md`, `self_model.md`, `sovereign.md` (read-only Sovereign→COO channel)

The investigation pipeline was two-phase: the model generated a Python script, it executed in a sandbox, the model interpreted the results.

---

## What Worked

**Operational architecture** — the containerised design was solid. Clean start/stop, full state persistence via volume mounts, graceful restart. The `stop-coo.sh` / `launch-coo.sh` pattern worked well.

**Staleness detection** — fingerprinting data between cycles and diverting stale modes to investigate/critique worked as intended. The COO didn't spin endlessly on observe when data hadn't changed.

**Investigation pipeline** — when scripts succeeded, they produced real findings. Session length by day of week, client transition patterns, task-level activity breakdowns were all genuinely novel outputs. The pipeline architecture (generate → execute → interpret) is sound.

**Activity trail** — the "Where You Left Off" summary (last 8 journal entries in compact form) provided basic cycle-to-cycle orientation.

**Agenda field** — after prompt strengthening, the COO reliably populated carry-forward questions. Specificity improved somewhat.

**AEDT timestamps** — after fixing the timezone handling in memory.py and the structlog processor, timestamps throughout memory files and logs correctly reflected local time.

**Sovereign channel** — `sovereign.md` as a read-only Sovereign→COO message channel worked cleanly. The COO read it on every cycle.

---

## What Failed

### 1. Prior belief override — the central failure

The COO's trained pattern-matching consistently defeated explicit instructions. After being told directly in `sovereign.md` that SEIFUKU dominance was intentional, the model continued producing entries like:

> *"the sustained lack of engagement with STAR and other categories suggests a potential misalignment with long-term goals"*

This persisted through multiple evolve cycles and explicit prompt directives ("treat Sovereign messages as ground truth"). The self-model was updated but the new understanding didn't propagate into observe/reflect cycles — each cycle pattern-matched from raw data back to the trained "imbalance" framing.

**Root cause**: llama3.3:70b cannot reliably override RLHF-trained response patterns with in-context instructions alone. This is a model capability ceiling, not a prompt problem. No amount of prompt engineering fully resolves it.

### 2. Verbatim repetition

Three consecutive observe entries at 09:50, 10:10, and 10:14 AEDT on 2026-03-08 were word-for-word identical. The staleness diversion should have caught this. Combined with the SEIFUKU framing problem, large portions of the journal are redundant text.

### 3. Investigation script failure rate

Roughly 40-50% of investigation scripts failed at runtime:
- `NameError` on `entries_to_dataframe` (not imported despite being in the helper)
- `KeyError` on DataFrame columns that didn't exist
- Empty DataFrames from queries (90-day queries likely exceeding data range)
- Syntax errors in generated code

The model was explicitly told to use `entries_to_dataframe()` in the prompt and still failed to import it consistently. When scripts succeeded, findings were real but narrow — the model kept returning to the same ~3 questions (SEIFUKU/STAR allocation, session length variability, untracked time) regardless of diversity prompts.

### 4. Topical fixation

Despite explicit "do not repeat questions from last 3 investigations" directives, the COO investigated SEIFUKU/STAR allocation dynamics in the large majority of its cycles. The Artemis tutoring mention in sovereign.md (a clear throwaway comment) was not fixated on — suggesting some editorial judgment exists, but topical diversity remained narrow.

### 5. Self-model shallow / no accumulation

The evolve mode ran as scheduled but produced surface-level self-model updates. The self-model after 5 days of operation looked nearly identical to its initial form — a generic paragraph about "repeating concerns without proposing concrete actions." No genuine development arc, no revised assumptions, no temporal narrative.

### 6. Zero Sovereign nudges

`should_act` was set to `true` zero times in the entire run. The COO never sent a message. This is partly appropriate (the data was genuinely stale for much of the run), but also reflects an overly conservative posture baked into the base model.

### 7. Agenda quality degraded under load

After prompt strengthening, the agenda briefly improved to specific bullet questions. Within a few cycles it collapsed back to a single vague line. The LLM treated agenda as the lowest-priority output field.

---

## Development Work Done During Run

Several improvements were shipped mid-run and represent learnings applicable to v2:

- **Staleness detection** — fingerprinting + diversion to investigate/critique when data unchanged
- **Stale-aware prompts** — separate prompt variants for each mode when data is stale
- **Duration parsing helpers** — `parse_duration_seconds()` and `entries_to_dataframe()` in `supabase_helper.py` to fix the most common script failure type
- **Activity trail** — compact 8-entry history at top of memory context
- **stop-coo.sh** — on-demand RAM release without data loss
- **Local timezone** — AEDT timestamps in logs and memory files
- **Agenda slot visibility** — shown even when empty to prompt model to fill it
- **Evolve in active hours** — added evolve to the active-hours schedule so self-model updates didn't wait for quiet hours
- **Cycle count in context** — temporal anchor for the model
- **Sovereign message directives** — explicit prompt instructions to treat sovereign.md as ground truth

---

## Quantitative Snapshot (final state)

| Metric | Value |
|--------|-------|
| Journal entries | ~50 (capped) |
| Hypothesis entries | ~20 (capped) |
| Investigation entries | ~15 (capped) |
| Sovereign nudges sent | 0 |
| Approx. script success rate | ~50-60% |
| Dominant investigation topic | SEIFUKU/STAR allocation |
| Self-model updates (meaningful) | ~0 |
| Agenda specificity (end state) | Low — single vague line |

---

## Architectural Verdict

The naive implementation is a valid proof-of-concept and established a working baseline. The container/volume/markdown architecture is clean and easy to reason about. The investigation pipeline is a genuine innovation worth keeping.

The fundamental limits are:

1. **Flat context-window memory** — all memory is text dumped into context. No retrieval, no relevance ranking, no real accumulation. As the journal fills, older insights become invisible.

2. **Single model, no reasoning** — one llama3.3:70b instance does everything. It cannot override its own trained priors. It has no chain-of-thought reasoning. Complex meta-instructions (integrate sovereign message, develop temporal self-model) are beyond its reliable capability.

3. **Generated code as tool use** — asking the model to write valid Python every cycle is fragile. ~40-50% failure rate is too high for a reliable analytical pipeline.

These are architectural issues. They set the ceiling for what prompt engineering alone can achieve, and that ceiling has been reached.
