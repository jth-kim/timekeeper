"""Custom hermes-compatible tools for COO Supabase data access.

These are registered with hermes-agent's tool system, giving the agent
the ability to query time-tracking data on demand rather than having
it pre-injected into the prompt.
"""

import json
from datetime import datetime, timedelta, timezone

import httpx

from config import SUPABASE_URL, SUPABASE_KEY, CONFIG_DIR, load_thresholds


def _headers() -> dict:
    return {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
    }


# --- Tool definitions in OpenAI function-calling format ---

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "get_current_timer",
            "description": "Get the currently running time-tracking timer, if any. Returns the active timer with client, project, description, tags, start time, and elapsed time.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_recent_entries",
            "description": "Get recent completed time entries from the tracking system. Each entry has: start, stop, duration (ISO format like PT1H30M), client_name, project_name, tags, description. Clients are identity-level: STAR (knowledge work), BBOY (physical), SEIFUKU (admin), BOJ (finance).",
            "parameters": {
                "type": "object",
                "properties": {
                    "hours": {
                        "type": "integer",
                        "description": "How many hours back to query (default 48)",
                        "default": 48,
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Max entries to return (default 100)",
                        "default": 100,
                    },
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_alert_thresholds",
            "description": "Get the alert threshold configuration. Contains goal_neglect (days before warning/alert per client), allocation (target percentages per client), anomaly (z-score thresholds), and cadence (nudge frequency limits).",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "send_nudge",
            "description": "Send a message/nudge to the Sovereign (the user) via Signal. Only use this when you have something specific and actionable to say. Most cycles you should stay silent.",
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "The message to send. Keep it short, direct, warm but not sycophantic.",
                    },
                },
                "required": ["message"],
            },
        },
    },
]


# --- Tool implementations ---

async def execute_tool(name: str, arguments: dict) -> str:
    """Execute a tool by name and return the result as a string."""
    if name == "get_current_timer":
        return await _get_current_timer()
    elif name == "get_recent_entries":
        return await _get_recent_entries(
            hours=arguments.get("hours", 48),
            limit=arguments.get("limit", 100),
        )
    elif name == "get_alert_thresholds":
        return _get_alert_thresholds()
    elif name == "send_nudge":
        return await _send_nudge(arguments.get("message", ""))
    else:
        return json.dumps({"error": f"Unknown tool: {name}"})


async def _get_current_timer() -> str:
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.get(
            f"{SUPABASE_URL}/rest/v1/current_timer_state",
            headers={**_headers(), "Accept-Profile": "live"},
            params={"state_key": "eq.primary", "select": "*"},
        )
        resp.raise_for_status()
        rows = resp.json()
        if rows:
            return json.dumps(rows[0], default=str)
        return json.dumps({"status": "No timer currently running"})


async def _get_recent_entries(hours: int = 48, limit: int = 100) -> str:
    since = (datetime.now(timezone.utc) - timedelta(hours=hours)).isoformat()
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.get(
            f"{SUPABASE_URL}/rest/v1/time_entries",
            headers=_headers(),
            params={
                "select": "start,stop,duration,client_name,project_name,tags,description",
                "start": f"gte.{since}",
                "order": "start.desc",
                "limit": str(limit),
            },
        )
        resp.raise_for_status()
        entries = resp.json()
        return json.dumps({
            "count": len(entries),
            "hours_queried": hours,
            "entries": entries,
        }, default=str)


def _get_alert_thresholds() -> str:
    thresholds = load_thresholds()
    if thresholds:
        return json.dumps(thresholds)
    return json.dumps({"error": "No thresholds config found"})


async def _send_nudge(message: str) -> str:
    from signal_client import send_message
    sent = await send_message(message)
    return json.dumps({"sent": sent, "message": message})
