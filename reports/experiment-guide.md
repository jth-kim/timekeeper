# Timekeeper COO — Experiment Guide

One-stop summary of all experiments run, what we learned, and where we're headed.

---

## Experiments

### 1. naive-coo (archived)

**Model**: llama3.3:70b | **Duration**: ~5 days | **Status**: archived

The proof-of-concept. Custom Python loop with 7-mode rotation (observe → reflect → plan → critique → hypothesise → investigate → evolve). Markdown-based memory, sandboxed Python investigation scripts, Supabase data access.

**What worked**: Container architecture, staleness detection, investigation pipeline (when scripts succeeded), activity trail, sovereign channel.

**What failed**: Prior belief override (model couldn't stop calling SEIFUKU dominance a "misalignment" despite explicit correction), verbatim repetition, ~40-50% script failure rate, topical fixation on SEIFUKU/STAR, shallow self-model, zero nudges sent.

**Verdict**: Valid baseline. Architecture is sound. Model capability is the ceiling — llama3.3:70b cannot reliably override trained priors or produce complex structured output.

**Full report**: `naive-coo-report.md`

---

### 2. qwen-nothink (archived)

**Model**: qwen3:30b-a3b (think: false) | **Duration**: ~11 hours | **Status**: archived

Control arm of the ABC test. Same custom architecture as naive-coo but with Qwen 3 and thinking explicitly disabled.

**Result**: 79% error rate. The model cannot produce valid JSON without thinking time. Only 3 of 8 memory files ever populated. Container restarted multiple times. Later cycles show the model writing prose observations instead of structured JSON — it understands the task but can't format the output.

**Verdict**: Thinking capacity is a prerequisite for structured output. Confirms that the mode-rotation architecture requires a model that can reason about format constraints while simultaneously reasoning about content.

**Full report**: See `abc-report.md` (combined report)

---

### 3. qwen-think (kept as history)

**Model**: qwen3:30b-a3b (think: true) | **Duration**: ~11 hours | **Status**: kept in repo

The strongest result so far. Same custom architecture, thinking enabled.

**What worked**: Genuine self-correction (caught a false "mislabelling crisis" it had fabricated), metacognitive self-model (3KB document tracking its own cognitive evolution), structured hypotheses with falsification criteria, self-modification (edited own config, created 5 tools, 23 scripts). All 8 memory file types populated, ~101KB total output.

**What failed**: Ruminative paralysis — after catching its own error, the agent spent ~35 cycles writing near-identical self-critique about its inability to fix its JSON generation process. The metacognitive capacity that enabled self-correction also enabled self-referential loops. Never sent a nudge; adopted deliberate silence posture.

**Key insight**: Think-mode + structured architecture produces depth that nothing else matched. The agent's self-model document and the false-alarm-to-self-correction arc are genuinely novel outputs. But the architecture provides no escape hatch from ruminative traps — once the agent decided it was "unreliable," it couldn't be talked out of it.

**Verdict**: Most promising direction. Needs loop-breaking mechanisms (cycle budgets on self-critique, forced mode advancement, external reset triggers).

**Full report**: See `abc-report.md`

---

### 4. qwen-hermes (invalid, pending rerun)

**Model**: qwen3:30b-a3b (think: true, by default) | **Duration**: ~11 hours | **Status**: needs rerun

NousResearch hermes-agent framework, cloned and driven programmatically.

**What happened**: Two integration bugs meant hermes ran without the COO identity (SOUL.md in wrong path) and without data tools (custom toolset not declared in hermes's toolset registry). The agent spent 11 hours writing timestamps to MEMORY.md. All 52 cycles produced identical boilerplate output.

**What we can still say**: Hermes's runtime stability is excellent (1 error in 52 cycles, 11 hours no restart). Its memory management works but is content-agnostic. The framework assumes model-driven initiative — without strong identity anchoring, the model defaulted to the most mechanical possible interpretation of its instructions.

**Verdict**: Experiment invalid. No conclusions about hermes architecture vs custom architecture. Rerun required with correct SOUL.md placement and tool registration.

**Full report**: `qwen-hermes-report.md`

---

## Cross-Cutting Findings

### Thinking capacity is necessary but not sufficient

| Config | Structured output | Self-correction | Depth | Stability |
|---|---|---|---|---|
| llama3.3:70b (no think) | Moderate (~50% scripts fail) | None (prior override) | Shallow | Moderate |
| qwen3:30b nothink | Broken (79% error rate) | N/A | Minimal | Poor |
| qwen3:30b think | Good (18% error rate) | Yes (caught false alarm) | Deep | Moderate |
| qwen3:30b + hermes | N/A (no tools) | N/A | None | Excellent |

### Architecture provides the floor, model provides the ceiling

The custom mode-rotation architecture forces structured cognition — without it, the model drifts into mechanical loops (hermes) or can't produce output at all (nothink). But the architecture can't make a model smarter than it is — llama3.3 hit a prior-override ceiling, and qwen3-think hit a ruminative-loop ceiling.

### The missing experiment

Hermes's stability + custom architecture's mode rotation + think-mode reasoning. The hypothesis: hermes's tool-calling infrastructure and memory management, combined with imposed cognitive structure and extended reasoning, would capture the best of all tested approaches.

---

## Repo Structure

```
timekeeper/
├── archive/              # Frozen experiments
│   ├── naive-coo/        # llama3.3:70b baseline
│   └── qwen-nothink/     # qwen3 without thinking (control)
├── qwen-think/           # qwen3 with thinking (kept as history)
├── qwen-hermes/          # hermes framework (pending rerun)
├── reports/              # All performance reports
│   ├── experiment-guide.md    # This file
│   ├── naive-coo-report.md   # naive-coo post-mortem
│   ├── abc-report.md         # ABC test comparative report
│   └── qwen-hermes-report.md # Hermes-specific post-mortem
├── config/               # Shared COO identity (mounted read-only into all experiments)
│   ├── coo_identity.md
│   ├── system_prompt.md
│   ├── system_prompt_inner.md
│   └── thresholds.toml
├── scripts/              # Shared operational scripts
├── hermes-strategy.md    # Hermes architecture analysis
└── v2-strategy.md        # V2 design strategy
```
