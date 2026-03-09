# Epoch 2 — Qwen 4-Way Run (Planned)

This archive slot is reserved for the next experiment epoch.

## Active experiment dirs (run from repo root)

- `qwen-think` (self-mod ON)
- `qwen-think-noselfmod` (self-mod OFF)
- `qwen-hermes` (self-mod ON)
- `qwen-hermes-noselfmod` (self-mod OFF)

## Purpose

Evaluate architecture (`think` vs `hermes`) and self-modification (`on` vs `off`) under the same base model (`qwen3:30b-a3b`) and same new COO identity prompt.

## Notes

- Self-mod gate is controlled by `SELF_MOD_ENABLED` in each experiment `.env`.
- Each experiment has its own `config/` folder mounted to `/data/config`.
- Config mount is writable only when `SELF_MOD_ENABLED=true`.

After the run, copy logs/reports/artifacts from root experiment dirs into this archive folder.
