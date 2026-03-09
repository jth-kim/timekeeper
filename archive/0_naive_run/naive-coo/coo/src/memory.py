"""Memory system — markdown-based persistent memory for the COO.

Files:
  journal.md      — timestamped stream of consciousness (last 50 entries)
  reflections.md  — pattern notes from reflect mode (last 20 entries)
  priorities.md   — working model of what matters (overwritten during plan mode)
  self_critique.md — performance self-review (last 20 entries)
  hypotheses.md   — active hypotheses about user patterns (last 20 entries)
  self_model.md   — the COO's evolving narrative understanding of itself
  agenda.md       — questions and threads to carry between cycles
"""

from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

from config import MEMORY_DIR, CONFIG_DIR, USER_TIMEZONE

# Entry caps per file
CAPS = {
    "journal.md": 50,
    "reflections.md": 20,
    "self_critique.md": 20,
    "hypotheses.md": 20,
    "investigations.md": 15,
}

# Use a distinctive separator that won't appear in LLM output
ENTRY_SEPARATOR = "\n<!-- entry -->\n"


def _ensure_dir():
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)


def read_file(name: str) -> str:
    """Read a memory file. Returns empty string if it doesn't exist."""
    path = MEMORY_DIR / name
    if path.exists():
        return path.read_text()
    return ""


# Files that only the Sovereign can write to
READ_ONLY_FILES = {"sovereign.md"}


def write_file(name: str, content: str) -> None:
    """Overwrite a memory file entirely (used for priorities.md)."""
    if name in READ_ONLY_FILES:
        return
    _ensure_dir()
    (MEMORY_DIR / name).write_text(content)


def append_entry(name: str, content: str) -> None:
    """Append a timestamped entry to a memory file, pruning if over cap."""
    if name in READ_ONLY_FILES:
        return
    _ensure_dir()
    path = MEMORY_DIR / name

    try:
        tz = ZoneInfo(USER_TIMEZONE)
    except Exception:
        tz = timezone.utc
    timestamp = datetime.now(tz).strftime("%Y-%m-%d %H:%M %Z")
    entry = f"### {timestamp}\n\n{content}"

    existing = path.read_text() if path.exists() else ""

    if existing.strip():
        entries = _split_entries(existing)
    else:
        entries = []

    entries.append(entry)

    cap = CAPS.get(name, 50)
    if len(entries) > cap:
        entries = entries[-cap:]

    path.write_text(ENTRY_SEPARATOR.join(entries) + "\n")


def _split_entries(text: str) -> list[str]:
    """Split a memory file into individual entries by separator."""
    # Support both old and new separators for migration
    if "<!-- entry -->" in text:
        parts = text.split("<!-- entry -->")
    else:
        # Legacy: split on markdown heading timestamps as a fallback
        import re
        parts = re.split(r"(?=^### \d{4}-\d{2}-\d{2})", text, flags=re.MULTILINE)
    return [p.strip() for p in parts if p.strip()]


def read_recent(name: str, n: int = 5) -> str:
    """Read the last n entries from a memory file."""
    text = read_file(name)
    if not text.strip():
        return ""
    entries = _split_entries(text)
    recent = entries[-n:]
    return ENTRY_SEPARATOR.join(recent)


# --- Config self-editing ---

EDITABLE_CONFIGS = {
    "system_prompt_inner.md",
    "coo_identity.md",
}


def read_config(name: str) -> str:
    """Read a config file. Returns empty string if it doesn't exist."""
    path = CONFIG_DIR / name
    if path.exists():
        return path.read_text()
    return ""


def write_config(name: str, content: str) -> bool:
    """Write to an editable config file. Returns False if file is not in the allow-list."""
    if name not in EDITABLE_CONFIGS:
        return False
    path = CONFIG_DIR / name
    # Keep a backup before overwriting
    if path.exists():
        backup = CONFIG_DIR / f"{name}.bak"
        backup.write_text(path.read_text())
    path.write_text(content)
    return True


def read_recent_logs(n: int = 10) -> str:
    """Read the last n lines from the COO log for operational self-awareness."""
    from config import LOG_DIR
    log_path = LOG_DIR / "coo.jsonl"
    if not log_path.exists():
        return ""
    lines = log_path.read_text().strip().split("\n")
    recent = lines[-n:]
    return "\n".join(recent)
