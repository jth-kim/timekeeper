"""Supabase helper for COO investigation scripts.

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
    """Read a COO memory file by name (e.g., 'journal.md')."""
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
    iso_match = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+(?:\.\d+)?)S)?$", s)
    if iso_match:
        h = int(iso_match.group(1) or 0)
        m = int(iso_match.group(2) or 0)
        sec = float(iso_match.group(3) or 0)
        return sign * (h * 3600 + m * 60 + sec)

    # HH:MM:SS or HH:MM
    time_match = re.match(r"(\d+):(\d+)(?::(\d+(?:\.\d+)?))?$", s)
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
