# Epoch 2 Plan — 4-Way Qwen Run

## Objective

Measure architecture and self-modification effects under the same model (`qwen3:30b-a3b`) and the new COO identity prompt.

## Arms

1. `qwen-think` (self-mod ON)
2. `qwen-think-noselfmod` (self-mod OFF)
3. `qwen-hermes` (self-mod ON)
4. `qwen-hermes-noselfmod` (self-mod OFF)

## Runtime Controls

- Same model and context settings unless intentionally changed in `.env`
- Same Supabase data source
- Same baseline prompt files copied from `config/`
- `SELF_MOD_ENABLED` controls both runtime guardrails and config mount mode

## Primary Metrics

1. Cycle completion and error rate
2. Real data access rate (timer/recent-entry tool usage)
3. Repetition/degradation rate across consecutive cycles
4. Investigation novelty (new questions vs repeated angles)
5. Action quality (specific, evidence-based nudges; not just count)

## Validity Gates

- Hermes must load COO identity from `SOUL.md` (not default Hermes persona)
- Hermes must expose and call timekeeper tools
- Self-mod OFF arms must show no config edits applied
- Self-mod ON arms must be able to apply config edits (at least capability-level)
