"""Configuration from environment variables and config files."""

import os
from pathlib import Path

import tomli


def _env(key: str, default: str | None = None) -> str:
    val = os.environ.get(key, default)
    if val is None:
        raise RuntimeError(f"Missing required env var: {key}")
    return val


# --- Supabase ---
SUPABASE_URL = _env("SUPABASE_URL")
SUPABASE_KEY = _env("SUPABASE_KEY")

# --- Ollama (via OpenAI-compatible endpoint) ---
OLLAMA_BASE_URL = _env("OLLAMA_BASE_URL", "http://host.containers.internal:11434")
OLLAMA_MODEL = _env("OLLAMA_MODEL", "qwen3:30b-a3b")

# --- Signal messaging ---
SIGNAL_ENABLED = _env("SIGNAL_ENABLED", "false").lower() == "true"

# --- Paths (inside container) ---
LOG_DIR = Path(_env("LOG_DIR", "/data/logs"))
STATE_DIR = Path(_env("STATE_DIR", "/data/state"))
CONFIG_DIR = Path(_env("CONFIG_DIR", "/data/config"))

# --- Loop cadence ---
CHECK_INTERVAL_SECONDS = int(_env("CHECK_INTERVAL_SECONDS", "1800"))
THINK_COOLDOWN_SECONDS = int(_env("THINK_COOLDOWN_SECONDS", "120"))

# --- Time awareness ---
USER_TIMEZONE = _env("USER_TIMEZONE", "Australia/Sydney")
ACTIVE_HOURS_START = int(_env("ACTIVE_HOURS_START", "6"))
ACTIVE_HOURS_END = int(_env("ACTIVE_HOURS_END", "23"))

# --- Hermes state ---
HERMES_HOME = Path(_env("HERMES_HOME", "/data/hermes"))

# --- Workspace ---
WORKSPACE_DIR = Path(_env("WORKSPACE_DIR", "/data/workspace"))


def load_thresholds() -> dict:
    """Load alert thresholds from config file."""
    path = CONFIG_DIR / "thresholds.toml"
    if path.exists():
        with open(path, "rb") as f:
            return tomli.load(f)
    return {}
