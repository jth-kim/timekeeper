"""Supabase client — the COO's only data source.

Reads live timer state and recent entries. All reasoning
happens in the LLM, not here.
"""

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import httpx

from config import SUPABASE_URL, SUPABASE_KEY, STATE_DIR

STATE_FILE = STATE_DIR / "coo_state.json"


def _headers() -> dict:
    return {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
    }


async def get_current_timer(client: httpx.AsyncClient) -> dict | None:
    """What's running right now?"""
    resp = await client.get(
        f"{SUPABASE_URL}/rest/v1/current_timer_state",
        headers={**_headers(), "Accept-Profile": "live"},
        params={"state_key": "eq.primary", "select": "*"},
    )
    resp.raise_for_status()
    rows = resp.json()
    return rows[0] if rows else None


async def get_recent_entries(
    client: httpx.AsyncClient, hours: int = 48
) -> list[dict]:
    """Recent completed time entries."""
    resp = await client.get(
        f"{SUPABASE_URL}/rest/v1/time_entries",
        headers=_headers(),
        params={
            "select": "start,stop,duration,client_name,project_name,tags,description",
            "start": f"gte.{(datetime.now(timezone.utc) - timedelta(hours=hours)).isoformat()}",
            "order": "start.desc",
            "limit": "100",
        },
    )
    resp.raise_for_status()
    return resp.json()


# --- Local state persistence ---

def load_state() -> dict:
    """Load persistent COO state from disk."""
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {
        "last_check_utc": None,
        "last_nudge_utc": None,
        "conversation_summary": "",
        "alert_history": [],
    }


def save_state(state: dict) -> None:
    """Save COO state to disk."""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2, default=str))
