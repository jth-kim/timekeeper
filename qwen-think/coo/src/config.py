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

# --- Ollama ---
OLLAMA_BASE_URL = _env("OLLAMA_BASE_URL", "http://host.containers.internal:11434")
OLLAMA_MODEL = _env("OLLAMA_MODEL", "qwen3:30b-a3b")
OLLAMA_THINK = _env("OLLAMA_THINK", "true").lower() == "true"
OLLAMA_NUM_CTX = int(_env("OLLAMA_NUM_CTX", "32768"))
OLLAMA_READ_TIMEOUT = float(_env("OLLAMA_READ_TIMEOUT", "600"))

# --- Signal messaging ---
SIGNAL_ENABLED = _env("SIGNAL_ENABLED", "false").lower() == "true"

# --- Paths (inside container) ---
LOG_DIR = Path(_env("LOG_DIR", "/data/logs"))
STATE_DIR = Path(_env("STATE_DIR", "/data/state"))
CONFIG_DIR = Path(_env("CONFIG_DIR", "/data/config"))

# --- Loop cadence ---
CHECK_INTERVAL_SECONDS = int(_env("CHECK_INTERVAL_SECONDS", "1800"))
THINK_COOLDOWN_SECONDS = int(_env("THINK_COOLDOWN_SECONDS", "60"))

# --- Time awareness ---
USER_TIMEZONE = _env("USER_TIMEZONE", "Australia/Sydney")
ACTIVE_HOURS_START = int(_env("ACTIVE_HOURS_START", "6"))   # local hour
ACTIVE_HOURS_END = int(_env("ACTIVE_HOURS_END", "23"))      # local hour

# --- Memory ---
MEMORY_DIR = Path(_env("MEMORY_DIR", "/data/memory"))

# --- Workspace (investigation sandbox) ---
WORKSPACE_DIR = Path(_env("WORKSPACE_DIR", "/data/workspace"))
SCRIPT_TIMEOUT_SECONDS = int(_env("SCRIPT_TIMEOUT_SECONDS", "30"))
STALE_CYCLE_THRESHOLD = int(_env("STALE_CYCLE_THRESHOLD", "3"))


def load_thresholds() -> dict:
    """Load alert thresholds from config file."""
    path = CONFIG_DIR / "thresholds.toml"
    if path.exists():
        with open(path, "rb") as f:
            return tomli.load(f)
    return {}
