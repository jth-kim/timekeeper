# How to Run Experiments

## Prerequisites

- Podman running (`podman machine start`)
- Ollama running with model pulled (`ollama pull qwen3:30b-a3b`)
- `.env` file in each experiment dir (e.g. `qwen-hermes/.env`)

## Quick Start — Run Everything

```bash
scripts/run-ab.sh
```

Builds and launches all experiments listed in the script. Edit `run-ab.sh` to add/remove experiments.

## Run a Single Experiment

```bash
# 1. One-time: ensure the podman network exists
scripts/setup-network.sh

# 2. Build the container image
scripts/build.sh qwen-hermes

# 3. Launch it
scripts/launch.sh qwen-hermes
```

Replace `qwen-hermes` with any experiment directory name.

## Monitoring

```bash
# Follow live logs
podman logs -f timekeeper-qwen-hermes

# Check container status
podman ps --filter "name=timekeeper"

# Cycle counts from structured log
podman exec timekeeper-qwen-hermes grep -c "cycle.complete" /data/logs/coo.jsonl
podman exec timekeeper-qwen-hermes grep -c "cycle.error" /data/logs/coo.jsonl

# Read the last log entry
podman exec timekeeper-qwen-hermes tail -1 /data/logs/coo.jsonl | python3 -m json.tool

# Check memory files (custom architecture)
podman exec timekeeper-qwen-think ls -la /data/memory/

# Check memory files (hermes)
podman exec timekeeper-qwen-hermes cat /data/hermes/memories/MEMORY.md
```

## Stopping

```bash
# Stop one
podman stop timekeeper-qwen-hermes

# Stop all timekeeper containers
podman stop $(podman ps --filter "name=timekeeper" -q)
```

State is persisted in `<experiment>/shared/` — restarting picks up where it left off.

## Clean Restart (wipe state)

```bash
podman stop timekeeper-qwen-hermes
podman rm timekeeper-qwen-hermes
rm -rf qwen-hermes/shared/logs/* qwen-hermes/shared/state/* qwen-hermes/shared/memory/*
# For hermes experiments, also:
rm -rf qwen-hermes/shared/hermes/memories/* qwen-hermes/shared/hermes/sessions/*
scripts/launch.sh qwen-hermes
```

## Podman VM Resources

Check current allocation:

```bash
podman machine inspect --format '{{.Resources.CPUs}} CPUs, {{.Resources.Memory}}MB RAM'
```

Change (requires restart):

```bash
podman machine stop
podman machine set --cpus 12 --memory 98304
podman machine start
```

## Repo Layout

```
config/                   # Shared COO identity — mounted read-only into all experiments
├── coo_identity.md       #   who the COO is
├── system_prompt.md      #   outer system prompt
├── system_prompt_inner.md #  cognitive structure guidance
└── thresholds.toml       #   alert thresholds

scripts/                  # Shared operational scripts
├── build.sh              #   build one experiment: scripts/build.sh <name>
├── launch.sh             #   launch one experiment: scripts/launch.sh <name>
├── setup-network.sh      #   create podman network (one-time)
└── run-ab.sh             #   build + launch all experiments

<experiment>/             # Each experiment directory
├── .env                  #   environment variables (model, cooldown, etc.)
├── coo/                  #   source code + Containerfile
│   ├── Containerfile
│   └── src/
└── shared/               #   runtime state (persists across restarts)
    ├── logs/
    ├── state/
    ├── memory/
    ├── workspace/
    └── hermes/           #   (hermes experiments only)
```

## Adding a New Experiment

1. Create a directory: `mkdir -p new-experiment/coo/src`
2. Add a `Containerfile` and source code in `coo/`
3. Copy and adjust `.env` from an existing experiment
4. If it needs hermes state: `mkdir -p new-experiment/shared/hermes`
5. Build and launch: `scripts/build.sh new-experiment && scripts/launch.sh new-experiment`
