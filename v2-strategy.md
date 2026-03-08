# Persistent LLM Agent — V2 Strategy

## The Three Bottlenecks

The naive COO run identified three specific architectural limits, not prompt limits. V2 needs to address all three:

1. **Memory retrieval** — flat markdown files with context-window stuffing don't scale and can't retrieve what's relevant
2. **Model reasoning depth** — a single instruction-tuned model cannot reliably override its own trained priors or perform deep multi-step reasoning
3. **Tool reliability** — generating Python scripts for tool use has ~50% failure rate; typed tools are needed

---

## Bottleneck 1: Memory — Use Letta (MemGPT)

**What Letta does**: Hierarchical memory with three layers:
- **Working memory** — in-context, always visible (like our current system)
- **Recall storage** — full conversation/journal history, searchable by the agent via function calls
- **Archival storage** — long-term vector storage, semantically searchable

The key shift: instead of dumping last-N entries into context and hoping, the agent *decides* what to retrieve. It can query "what did I observe about BBOY patterns last week?" and get relevant entries back, rather than whatever happens to fit in the context window.

**Why this fixes the naive COO's problems**:
- Self-model accumulates rather than being overwritten each evolve cycle
- Sovereign messages are retrievable with context, not just the most recent one
- Investigation findings persist and are searchable — no more re-asking the same questions
- Temporal narrative becomes possible: the agent can recall how its understanding has changed over weeks, not just cycles

**Migration path**: Letta has a Python SDK and can run self-hosted. The existing memory files (journal.md, etc.) could be imported as initial archival memory. The agent identity/persona maps to Letta's persona system. The Sovereign channel maps to human-turn messages.

---

## Bottleneck 2: Model — Reasoning Model + Multi-Model Routing

**The prior override problem** cannot be solved with prompting alone. llama3.3:70b pattern-matches to trained outputs faster than it processes in-context instructions. The fix is a model that actually *thinks* before responding.

**QwQ-32B** (Qwen's reasoning model) is the most promising local option:
- Produces chain-of-thought reasoning traces before answering
- Much better at following complex meta-instructions
- Smaller (32B vs 70B) but outperforms 70B instruction-tuned models on reasoning tasks
- Runs locally via Ollama

**Multi-model routing** (pattern from oh-my-opencode):
Different modes have different requirements. Not every cycle needs a reasoning model — that would be slow and expensive. Route by task:

| Mode | Model | Rationale |
|------|-------|-----------|
| observe | Fast 7-14B model | Lightweight data read, low reasoning demand |
| reflect, hypothesize, critique | QwQ-32B or equivalent reasoning model | Needs genuine multi-step thought |
| evolve | Reasoning model | Self-modification requires careful reasoning |
| investigate (generate) | Code-capable model (Qwen2.5-Coder or similar) | Script generation needs code specialisation |
| investigate (interpret) | Fast model | Interpretation is straightforward |

This cuts reasoning model invocations to ~30% of cycles while applying depth where it matters.

**If running via API** (Claude Sonnet/Opus for evolve/reflect, fast model for observe): even more powerful, but requires internet-accessible deployment. Worth considering if moving off fully-local.

---

## Bottleneck 3: Tool Use — MCP-Style Typed Tools

**The problem**: Asking the model to generate valid Python every cycle is fragile. The model has to correctly remember import syntax, available functions, DataFrame column names, and error handling — every time. ~50% failure rate results.

**The fix**: Typed, validated MCP tools the model *calls* rather than *implements*.

Instead of:
> "Write a Python script that uses entries_to_dataframe() to get sessions by client..."

The model gets:
> Available tools: `get_sessions(days=30, client=None)`, `get_gaps(client=None)`, `get_session_distribution(by='day_of_week'|'hour'|'client')`

It calls them with arguments. The implementation is stable server-side. Failures are typed errors, not Python tracebacks.

**Skill-embedded MCPs** (from oh-my-opencode): scope MCP servers to modes, spin up on-demand. The investigate mode gets analytical data tools. The evolve mode gets memory-write tools. The observe mode gets a minimal read-only context tool. No global context bloat.

**Implementation path**: Build a small MCP server wrapping the Supabase queries. Start with 5-10 well-defined analytical tools covering the queries the COO actually needs. The investigation pipeline becomes: model selects tool + parameters → server executes → model interprets clean output.

---

## Primitives Worth Keeping from Naive COO

These worked and should survive into v2:

- **Investigation pipeline pattern** (generate question → execute → interpret) — keep the *structure*, replace the *mechanism* with MCP tools
- **Staleness detection** — fingerprinting data across cycles, diverting to deep thinking when data unchanged
- **Thinking mode schedule** — active vs. quiet hours, different mode distributions
- **Sovereign channel** — read-only human→agent message channel, surfaces in every cycle
- **Activity trail** — compact recent-history summary for cycle orientation
- **Container/volume architecture** — clean, portable, restartable

---

## Primitives Worth Extracting from the Research

From **Letta**: hierarchical memory, recall/archival search, persona system

From **oh-my-opencode**:
- Skill-embedded MCPs (scoped tools per mode, on-demand)
- Multi-model routing (right model for right task)
- Ralph Loop (iterate until verified complete — apply to investigation cycles)
- Hash-anchored edits (if building any code-editing capability)

From **Qwen ecosystem**: QwQ-32B as local reasoning model; Qwen2.5-Coder for script generation

From **lmcache**: KV cache reuse for long system prompts — worth applying to the identity/persona prompt which is static across cycles

---

## Suggested Build Order

**Phase 1 — Model swap** (lowest effort, highest leverage)
- Swap llama3.3:70b for QwQ-32B for deep modes (reflect, evolve, critique, hypothesize)
- Keep a fast model for observe and investigate-interpret
- Test whether prior override problem resolves

**Phase 2 — MCP tool layer**
- Build MCP server wrapping Supabase analytical queries
- Replace Python script generation with typed tool calls
- Target: 90%+ tool call success rate

**Phase 3 — Letta memory integration**
- Migrate to Letta for memory layer
- Import existing memory files as archival seed
- Implement recall/archival queries in the thinking loop

**Phase 4 — Routing + orchestration**
- Implement multi-model routing properly
- Skill-embedded MCPs per mode
- Consider LangGraph or lightweight orchestration for mode-to-mode flow

---

## Open Questions

- **Local vs. API**: Fully local (Ollama) preserves privacy and zero cost but caps model quality. A hybrid (local fast model + API for deep modes) may be the right balance.
- **Letta managed vs. self-hosted**: Managed is easier to start; self-hosted keeps data local. Given the sensitivity of time-tracking data, self-hosted preferred.
- **Heretic/uncensorship models**: Worth testing QwQ or Qwen with and without safety fine-tuning removed to see if instruction-following improves. Low priority until Phase 1 baseline is established.
- **Dashboard (Panopticon)**: The spec exists. Defer until v2 architecture is stable — a dashboard built on the naive stack will need rebuilding anyway.
