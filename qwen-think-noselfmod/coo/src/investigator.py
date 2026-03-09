"""Investigator — two-phase LLM cycle for the investigate mode.

Phase 1: Ask the LLM to generate a Python script to answer a question.
Phase 2: Execute the script, feed results back for interpretation.
"""

import httpx

from ollama_client import _call_ollama, _load_system_prompt, _strip_thinking


# Phase 1 prompt — script generation
GENERATE_PROMPT = """## Thinking Mode: INVESTIGATE

You have access to a Python execution environment. You can write and run scripts
to investigate the Sovereign's time-tracking data, build analytical tools, and
develop your operational capabilities.

### Available in your scripts:

```python
from supabase_helper import query_entries, query_current_timer, read_memory
from supabase_helper import parse_duration_seconds, entries_to_dataframe

# query_entries(days=30) -> list[dict]
#   Each entry has: start, stop, duration, client_name, project_name, tags, description
#   IMPORTANT: 'duration' is an ISO string like "PT1H30M" — NOT a number!
#   Use parse_duration_seconds(d) to convert, or use entries_to_dataframe() which handles it.

# entries_to_dataframe(entries) -> pd.DataFrame
#   Converts entries to a DataFrame with proper types:
#   - 'start'/'stop' as datetime, 'duration_seconds'/'duration_minutes'/'duration_hours' as float
#   ALWAYS use this instead of pd.DataFrame(entries) — it handles type conversion for you.

# parse_duration_seconds(duration_str) -> float
#   Converts "PT1H30M15S", "01:30:15", or numeric strings to seconds.

# query_current_timer() -> dict | None
#   Returns the currently running timer, if any

# read_memory(filename) -> str
#   Read your own memory files (e.g., 'journal.md', 'priorities.md')
```

Libraries available: `pandas`, `matplotlib`, `json`, `datetime`, `collections`, `statistics`, `pathlib`

CRITICAL: The 'duration' field from Supabase is an ISO string like "PT1H30M15S", NOT a number.
You MUST use `entries_to_dataframe()` or `parse_duration_seconds()` to work with durations.
Do NOT call `.sum()` or `.mean()` on the raw 'duration' column — it will fail or return 0.

For matplotlib: save figures to `/data/workspace/results/` (e.g., `plt.savefig('/data/workspace/results/my_chart.png')`)

You can also import from `/data/workspace/tools/` — modules you've previously built.

{workspace_context}

### Your task

Generate a Python script that investigates something genuinely useful for your role as COO.
Look at your recent investigations above — do NOT repeat a question you have already asked.
If your last 3 investigations were about SEIFUKU/STAR allocation, you MUST investigate something else.
Topical diversity is required. Each investigation should open a NEW angle.

Ideas (but develop your own questions):
- Session length patterns by time of day or day of week
- Client transition patterns (what follows what?)
- Gaps between sessions (untracked time analysis)
- Compare this week vs last week vs the week before
- Build a reusable analysis tool and save it to /data/workspace/tools/
- Investigate something specific from your agenda — a question you named, not a vague goal
- BOJ activity patterns, BBOY session timing, entry description analysis

Your script should print its findings to stdout in a clear, readable format.
Keep scripts focused — one question per script.

Respond in JSON:
{{"question": "What specific question are you investigating?", "script_name": "descriptive_name", "script_code": "the full Python script — must be valid Python", "description": "What this script does and why you chose this investigation"}}"""


# Phase 2 prompt — result interpretation
INTERPRET_PROMPT = """## Investigation Results

You asked: {question}
You ran: {script_name}

### Script output:
```
{stdout}
```
{stderr_section}

### Your task

Interpret these results. What did you learn? Be specific — reference actual numbers
from the output. What's surprising? What changes your understanding?

If the script failed, diagnose why and note what to fix next time.

If this script would be generally useful to run again (e.g., a weekly report generator),
recommend saving it as a tool.

Respond in JSON:
{{"finding": "What you learned — specific, grounded in the output numbers", "significance": "Why this matters for your role as COO — how does it change your priorities or understanding?", "next_question": "What follow-up investigation would build on this finding?", "should_save_tool": true/false, "tool_name": "name_if_saving (omit if not saving)", "agenda": "1-2 SPECIFIC questions this finding raises — 'Question: [concrete]? Test: [when/how].' Not generic goals."}}"""


async def generate_investigation(
    client: httpx.AsyncClient,
    data_context: str,
    memory_context: str,
    workspace_context: str,
) -> dict:
    """Phase 1: Ask the LLM to generate an investigation script.

    Returns dict with: question, script_name, script_code, description
    """
    import json

    system = _load_system_prompt(inner=True)
    prompt_text = GENERATE_PROMPT.format(workspace_context=workspace_context)

    user_content = f"""{prompt_text}

## Current Time-Tracking Data
{data_context}

## Your Memory
{memory_context if memory_context else "No memory yet — this is early in your operation."}"""

    raw = await _call_ollama(client, system, user_content, temperature=0.7, max_tokens=4096)

    try:
        result = _parse_json_response(raw)
        # Ensure script_code is present and non-empty
        if not result.get("script_code", "").strip():
            raise ValueError("Empty script_code in response")
        return result
    except (json.JSONDecodeError, IndexError, ValueError) as e:
        import structlog
        log = structlog.get_logger()
        log.warning("investigate.parse_failed", error=str(e), raw_preview=raw[:500])
        return {
            "question": "Failed to generate investigation",
            "script_name": "failed",
            "script_code": "",
            "description": f"LLM response could not be parsed: {raw[:300]}",
        }


async def interpret_results(
    client: httpx.AsyncClient,
    question: str,
    script_name: str,
    execution_result: dict,
    memory_context: str,
) -> dict:
    """Phase 2: Feed script results back to the LLM for interpretation.

    Returns dict with: finding, significance, next_question, should_save_tool, agenda
    """
    import json

    system = _load_system_prompt(inner=True)

    stderr_section = ""
    if execution_result.get("stderr"):
        stderr_section = f"\n### Errors:\n```\n{execution_result['stderr']}\n```"

    prompt_text = INTERPRET_PROMPT.format(
        question=question,
        script_name=script_name,
        stdout=execution_result.get("stdout", "(no output)"),
        stderr_section=stderr_section,
    )

    user_content = f"""{prompt_text}

## Your Memory
{memory_context if memory_context else "No prior context."}"""

    raw = await _call_ollama(client, system, user_content, temperature=0.4, max_tokens=2048)

    try:
        return _parse_json_response(raw)
    except (json.JSONDecodeError, IndexError):
        return {
            "finding": f"Could not parse interpretation: {raw[:200]}",
            "significance": "",
            "next_question": "",
            "should_save_tool": False,
            "agenda": "",
        }


def _parse_json_response(raw: str) -> dict:
    """Parse a JSON response from the LLM, handling markdown fences, thinking tags, and code in values."""
    import json
    import re

    cleaned = _strip_thinking(raw).strip()

    # Remove markdown fences
    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[1]
        cleaned = cleaned.rsplit("```", 1)[0]
        cleaned = cleaned.strip()

    # First try direct parsing
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    # The LLM often fails to properly escape code in JSON strings.
    # Try to extract fields manually if JSON parsing fails.
    result = {}

    # Extract simple string fields
    for field in ("question", "script_name", "description", "finding",
                  "significance", "next_question", "tool_name", "agenda"):
        match = re.search(rf'"{field}"\s*:\s*"((?:[^"\\]|\\.)*)"', cleaned)
        if match:
            result[field] = match.group(1).replace('\\"', '"').replace('\\n', '\n')

    # Extract boolean fields
    for field in ("should_save_tool",):
        match = re.search(rf'"{field}"\s*:\s*(true|false)', cleaned, re.IGNORECASE)
        if match:
            result[field] = match.group(1).lower() == "true"

    # Extract script_code — this is the tricky one. Look for the value between
    # "script_code": " and the closing quote (accounting for escaped quotes)
    code_match = re.search(r'"script_code"\s*:\s*"((?:[^"\\]|\\.)*)"', cleaned, re.DOTALL)
    if code_match:
        code = code_match.group(1)
        # Unescape
        code = code.replace('\\n', '\n').replace('\\t', '\t').replace('\\"', '"').replace('\\\\', '\\')
        result["script_code"] = code

    if result:
        return result

    raise json.JSONDecodeError("Could not extract fields from response", cleaned, 0)
