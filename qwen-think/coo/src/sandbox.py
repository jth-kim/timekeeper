"""Sandbox — workspace management and script execution for the COO.

The COO can write Python scripts, execute them in a subprocess,
and read the results. Scripts have access to Supabase via a
helper module and can use pandas/matplotlib for analysis.

Directory structure:
  /data/workspace/
    scripts/      — timestamped generated scripts
    results/      — script outputs (JSON, CSV, PNG)
    tools/        — reusable modules the COO promotes from scripts
    lib/          — auto-generated supabase_helper.py
"""

import ast
import os
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

from config import WORKSPACE_DIR, SCRIPT_TIMEOUT_SECONDS

SCRIPTS_DIR = WORKSPACE_DIR / "scripts"
RESULTS_DIR = WORKSPACE_DIR / "results"
TOOLS_DIR = WORKSPACE_DIR / "tools"
LIB_DIR = WORKSPACE_DIR / "lib"

MAX_OUTPUT_BYTES = 50_000
MAX_SCRIPT_SIZE = 10_000

# The supabase_helper.py that gets auto-generated into workspace/lib/
# Scripts can `from supabase_helper import query_entries` to access data.
_SUPABASE_HELPER_CODE = '''"""Supabase helper for COO investigation scripts.

Auto-generated — do not edit manually. Regenerated on each COO restart.

Usage:
    from supabase_helper import query_entries, query_current_timer, read_memory
"""

import os
from datetime import datetime, timezone, timedelta

import httpx

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]
MEMORY_DIR = os.environ.get("MEMORY_DIR", "/data/memory")

_HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
}


def query_entries(days: int = 30, limit: int = 500) -> list[dict]:
    """Query time entries from Supabase.

    Args:
        days: How many days back to query (default 30).
        limit: Max entries to return (default 500).

    Returns:
        List of time entry dicts with keys:
        start, stop, duration, client_name, project_name, tags, description
    """
    since = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
    resp = httpx.get(
        f"{SUPABASE_URL}/rest/v1/time_entries",
        headers=_HEADERS,
        params={
            "select": "start,stop,duration,client_name,project_name,tags,description",
            "start": f"gte.{since}",
            "order": "start.desc",
            "limit": str(limit),
        },
        timeout=30.0,
    )
    resp.raise_for_status()
    return resp.json()


def query_current_timer() -> dict | None:
    """Get the currently running timer, if any."""
    headers = {**_HEADERS, "Accept-Profile": "live"}
    resp = httpx.get(
        f"{SUPABASE_URL}/rest/v1/current_timer_state",
        headers=headers,
        params={"state_key": "eq.primary", "select": "*"},
        timeout=30.0,
    )
    resp.raise_for_status()
    rows = resp.json()
    return rows[0] if rows else None


def read_memory(filename: str) -> str:
    """Read a COO memory file by name (e.g., \'journal.md\')."""
    path = os.path.join(MEMORY_DIR, filename)
    if os.path.exists(path):
        with open(path) as f:
            return f.read()
    return ""


def parse_duration_seconds(duration_str: str) -> float:
    """Parse an ISO 8601 duration string (e.g., 'PT1H30M15S', '-PT2H', '01:30:15') to seconds.

    Handles formats returned by Supabase/Toggl:
    - ISO 8601: PT1H30M15S, PT45M, PT30S, -PT2H
    - HH:MM:SS: 01:30:15, -02:00:00
    - Already numeric: 3600, 3600.0

    Returns float seconds. Negative durations return negative values.
    """
    import re

    if isinstance(duration_str, (int, float)):
        return float(duration_str)

    s = str(duration_str).strip()
    if not s:
        return 0.0

    # Try numeric first
    try:
        return float(s)
    except ValueError:
        pass

    # Handle sign
    sign = 1
    if s.startswith("-"):
        sign = -1
        s = s[1:]

    # ISO 8601: PT1H30M15S
    iso_match = re.match(r"PT(?:(\\d+)H)?(?:(\\d+)M)?(?:(\\d+(?:\\.\\d+)?)S)?$", s)
    if iso_match:
        h = int(iso_match.group(1) or 0)
        m = int(iso_match.group(2) or 0)
        sec = float(iso_match.group(3) or 0)
        return sign * (h * 3600 + m * 60 + sec)

    # HH:MM:SS or HH:MM
    time_match = re.match(r"(\\d+):(\\d+)(?::(\\d+(?:\\.\\d+)?))?$", s)
    if time_match:
        h = int(time_match.group(1))
        m = int(time_match.group(2))
        sec = float(time_match.group(3) or 0)
        return sign * (h * 3600 + m * 60 + sec)

    return 0.0


def entries_to_dataframe(entries: list[dict]) -> "pd.DataFrame":
    """Convert time entries to a pandas DataFrame with proper types.

    Automatically:
    - Converts 'start' and 'stop' to datetime
    - Converts 'duration' to numeric seconds via parse_duration_seconds
    - Adds 'duration_minutes' and 'duration_hours' columns

    Usage:
        from supabase_helper import query_entries, entries_to_dataframe
        df = entries_to_dataframe(query_entries(days=14))
    """
    import pandas as pd

    df = pd.DataFrame(entries)
    if df.empty:
        return df

    if "start" in df.columns:
        df["start"] = pd.to_datetime(df["start"], utc=True)
    if "stop" in df.columns:
        df["stop"] = pd.to_datetime(df["stop"], utc=True)
    if "duration" in df.columns:
        df["duration_seconds"] = df["duration"].apply(parse_duration_seconds)
        df["duration_minutes"] = df["duration_seconds"] / 60
        df["duration_hours"] = df["duration_seconds"] / 3600

    return df
'''


def ensure_workspace() -> None:
    """Create workspace directory structure and write helper modules."""
    for d in (SCRIPTS_DIR, RESULTS_DIR, TOOLS_DIR, LIB_DIR):
        d.mkdir(parents=True, exist_ok=True)

    # Write/update the supabase helper
    helper_path = LIB_DIR / "supabase_helper.py"
    helper_path.write_text(_SUPABASE_HELPER_CODE)

    # Clear pycache to ensure updated helper is used
    pycache = LIB_DIR / "__pycache__"
    if pycache.exists():
        import shutil
        shutil.rmtree(pycache)

    # Write __init__.py for lib/ so it's importable
    init_path = LIB_DIR / "__init__.py"
    if not init_path.exists():
        init_path.write_text("")


def write_script(name: str, code: str, description: str) -> Path:
    """Write a Python script to the scripts directory.

    Args:
        name: Short descriptive name (will be slugified).
        code: The Python source code.
        description: What this script does.

    Returns:
        Path to the written script.

    Raises:
        ValueError: If script is too large.
    """
    if len(code) > MAX_SCRIPT_SIZE:
        raise ValueError(f"Script too large ({len(code)} bytes, max {MAX_SCRIPT_SIZE})")

    # Validate syntax before writing
    try:
        ast.parse(code)
    except SyntaxError:
        pass  # Let the execution phase catch it with a proper error message

    slug = name.replace(" ", "_").replace("/", "_").lower()[:50]
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{slug}.py"
    path = SCRIPTS_DIR / filename

    header = f'"""Investigation: {description}\nGenerated: {timestamp} UTC\n"""\n\n'
    path.write_text(header + code)

    return path


def execute_script(script_path: Path) -> dict:
    """Execute a Python script in a subprocess with timeout and output caps.

    Returns:
        dict with keys: success, stdout, stderr, returncode, duration_seconds
    """
    env = {
        **os.environ,
        "PYTHONPATH": str(LIB_DIR),
    }

    start = time.monotonic()
    try:
        result = subprocess.run(
            ["python", str(script_path)],
            capture_output=True,
            text=True,
            timeout=SCRIPT_TIMEOUT_SECONDS,
            cwd=str(WORKSPACE_DIR),
            env=env,
        )
        duration = round(time.monotonic() - start, 1)

        stdout = result.stdout[:MAX_OUTPUT_BYTES]
        stderr = result.stderr[:MAX_OUTPUT_BYTES]

        if len(result.stdout) > MAX_OUTPUT_BYTES:
            stdout += f"\n... (truncated, {len(result.stdout)} total bytes)"
        if len(result.stderr) > MAX_OUTPUT_BYTES:
            stderr += f"\n... (truncated, {len(result.stderr)} total bytes)"

        return {
            "success": result.returncode == 0,
            "stdout": stdout,
            "stderr": stderr,
            "returncode": result.returncode,
            "duration_seconds": duration,
        }

    except subprocess.TimeoutExpired:
        duration = round(time.monotonic() - start, 1)
        return {
            "success": False,
            "stdout": "",
            "stderr": f"Script timed out after {SCRIPT_TIMEOUT_SECONDS}s",
            "returncode": -1,
            "duration_seconds": duration,
        }

    except Exception as e:
        duration = round(time.monotonic() - start, 1)
        return {
            "success": False,
            "stdout": "",
            "stderr": f"Execution error: {e}",
            "returncode": -1,
            "duration_seconds": duration,
        }


def list_tools() -> list[dict]:
    """List reusable tools the COO has built in the tools/ directory."""
    tools = []
    if not TOOLS_DIR.exists():
        return tools

    for path in sorted(TOOLS_DIR.glob("*.py")):
        if path.name.startswith("_"):
            continue
        # Read first docstring for description
        try:
            source = path.read_text()
            tree = ast.parse(source)
            docstring = ast.get_docstring(tree) or "No description"
        except Exception:
            docstring = "Could not parse"

        tools.append({
            "name": path.name,
            "description": docstring.split("\n")[0],  # First line only
            "last_modified": datetime.fromtimestamp(
                path.stat().st_mtime, tz=timezone.utc
            ).strftime("%Y-%m-%d %H:%M UTC"),
        })

    return tools


def get_script_history(n: int = 10) -> str:
    """Get a formatted summary of recent scripts for LLM context."""
    if not SCRIPTS_DIR.exists():
        return ""

    scripts = sorted(SCRIPTS_DIR.glob("*.py"), key=lambda p: p.stat().st_mtime, reverse=True)[:n]

    if not scripts:
        return ""

    lines = []
    for path in scripts:
        try:
            source = path.read_text()
            tree = ast.parse(source)
            docstring = ast.get_docstring(tree) or "No description"
            desc = docstring.split("\n")[0]
        except Exception:
            desc = "Could not parse"

        lines.append(f"- {path.name}: {desc}")

    return "\n".join(lines)
