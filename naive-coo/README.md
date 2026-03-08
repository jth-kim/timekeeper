# Timekeeper COO

Persistent agent on the Mac Studio. Reads from Supabase (live timer + entries),
reasons via Ollama, nudges via Signal.

## Setup

```bash
bash scripts/setup-network.sh
cp .env.example .env   # fill in real values
bash scripts/build-coo.sh
bash scripts/launch-coo.sh
```

## Structure

```
coo/src/           — agent source (loop, supabase client, ollama client, signal stub)
config/            — system prompt + thresholds (mounted read-only into container)
shared/logs/       — structured JSON logs (mounted into container)
shared/state/      — persistent state across restarts (mounted into container)
scripts/           — setup, build, launch
```

## No Toggl API needed

Everything comes from Supabase — the sync pipeline handles Toggl ingestion.
The COO reads `live.current_timer_state` and `public.time_entries`.
