"""Ollama client for COO reasoning and thinking."""

import httpx
import json
from pathlib import Path

from config import OLLAMA_BASE_URL, OLLAMA_MODEL, CONFIG_DIR


def _load_identity() -> str:
    """Load the COO identity anchor from config mount."""
    path = CONFIG_DIR / "coo_identity.md"
    if path.exists():
        return path.read_text()
    return ""


def _load_system_prompt(inner: bool = False) -> str:
    """Load the COO system prompt from config mount, with identity anchor prepended.

    Args:
        inner: If True, load the inner-thinking prompt (reflect/plan/critique/hypothesize).
               If False, load the observe/user-facing prompt.
    """
    identity = _load_identity()

    if inner:
        prompt_path = CONFIG_DIR / "system_prompt_inner.md"
        if prompt_path.exists():
            role_prompt = prompt_path.read_text()
            return f"{identity}\n\n---\n\n{role_prompt}" if identity else role_prompt
    prompt_path = CONFIG_DIR / "system_prompt.md"
    if prompt_path.exists():
        role_prompt = prompt_path.read_text()
        return f"{identity}\n\n---\n\n{role_prompt}" if identity else role_prompt
    return (
        "You are the COO of a personal productivity system. "
        "You observe time-tracking data and decide whether to nudge the user. "
        "Be concise. Only speak when you have something specific to say."
    )

# Modes that use the inner (self-talk) system prompt
_INNER_MODES = {"reflect", "plan", "critique", "hypothesize", "evolve", "investigate"}


def _parse_json_response(raw: str) -> dict:
    """Parse a JSON response from the LLM, handling markdown fences."""
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[1]
        cleaned = cleaned.rsplit("```", 1)[0]
    return json.loads(cleaned)


# --- Mode-specific prompts ---

MODE_PROMPTS = {
    "observe": """## Thinking Mode: OBSERVE

Structure your thinking into these four sections:

**ground**: What do you actually see in the data right now? Specific numbers only — elapsed time, session count, hours today, time since last transition. If nothing changed since your last entry, say "No change." and keep it to one sentence.

**tension**: What's surprising, off, or puzzling? What doesn't fit your expectations? What's missing that should be there? If there's no tension, what assumption are you making that might be wrong? This is the most important section — it's where insight starts. For any pattern you name: how long has it been true? Is it intensifying, stable, or fading? Duration is signal — three days of something is a different situation from three hours of it.

**synthesis**: Given the ground and the tension, what's your current read? What do you think is happening? What's your posture — and does anything warrant speaking to the Sovereign?

**agenda** (REQUIRED): What 2-3 specific, testable questions do you want to carry into your next cycle? Bad: "investigate imbalances." Good: "Does a SEIFUKU session >2h reliably precede a STAR session? Check the next 24h." Never leave this vague or empty.

Rules:
- Do NOT rewrite your previous observation in different words. If the ground hasn't changed, say so in one line and spend your space on tension and synthesis.
- A good observe entry develops a thought across these sections, not just labels the data.
- If the Sovereign has left you a message (see "Message from the Sovereign" in your memory), you MUST incorporate it. Do not contradict what you have been directly told. If they explained a pattern, treat that explanation as ground truth — not as one hypothesis among many.

Respond in JSON:
{{"ground": "What you see — specific numbers, one paragraph", "tension": "What's surprising, missing, or doesn't fit — one to two paragraphs", "synthesis": "Your read on the situation and posture — one to two paragraphs", "should_act": true/false, "message": "Message to Sovereign if should_act", "agenda": "2-3 SPECIFIC testable questions for next cycle — never generic, never empty"}}""",

    "reflect": """## Thinking Mode: REFLECT

This is your deepest thinking mode. Structure it carefully:

**ground**: Lay out the specific data you're working from. Do the arithmetic. What are the actual hours per client? Session counts? Average durations? Ratios? Don't narrate — compute. This is your evidence base.

**tension**: Now look for what DOESN'T fit. Where are the contradictions, absences, surprises?
- What would you expect to see that isn't there?
- What patterns break when you look closely at the numbers?
- Where does the story the data tells conflict with your prior understanding?
- What's in the gaps between entries — the untracked time?
- Look at your agenda and prior reflections: have any of your earlier questions been answered, or deepened?

**possibility**: Generate multiple interpretations. Don't collapse to one explanation — hold at least two or three in mind:
- What are different ways to read the patterns you see?
- What would the optimistic interpretation be? The concerning one?
- What can't you determine from the data alone — what's genuinely ambiguous?
- If you could ask the Sovereign one question, what would it be and why?

**synthesis**: Now integrate. Given the ground, the tensions, and the possibilities:
- What's your best current understanding of what's happening?
- What has CHANGED in your understanding since your last reflection?
- What are you more certain about? Less certain about?
- What should guide your observations and priorities going forward?

Write at length in each section. A good reflection is several paragraphs total. If it sounds like your previous reflections, you are failing. Go deeper or sideways.

If the Sovereign has left you a message, treat it as ground truth. Do not re-frame what they told you as "one possible interpretation." If they explained why something looks the way it does, your reflection must build from that — not around it.

Respond in JSON:
{{"ground": "Data and arithmetic — specific numbers, computations, evidence", "tension": "Contradictions, absences, surprises — multiple paragraphs", "possibility": "Multiple interpretations held in parallel — at least 2-3", "synthesis": "Integration and updated understanding — what changed, what's next", "should_act": false, "message": "", "agenda": "2-3 SPECIFIC open questions this reflection raises — name the question and when/how you'd test it"}}""",

    "plan": """## Thinking Mode: PLAN

Update your working priorities. This replaces your current priorities file. Structure it as:

**situation**: Brief, specific assessment of where things stand right now. Time of day, what's active, what's recent. One paragraph with numbers.

**tensions**: What are the key uncertainties or concerns? What could go either way? What are you watching? Not generic ("balance across clients") but specific ("STAR has been absent 48h and tomorrow morning is the test").

**intentions**: Given the situation and tensions, what is your plan?
- What specific events or thresholds would make you speak to the Sovereign?
- What's your posture: watchful, supportive, hands-off, concerned, probing?
- What are you choosing NOT to act on, and why?
- What open questions from your reflections should guide your next observations?

**self_check**: Before finalizing — is this plan actually different from your last one? Is it specific enough that you could be WRONG about something in it? If it's generic enough to be right no matter what happens, it's useless. Rewrite it.

Respond in JSON:
{{"situation": "Where things stand — specific, with numbers", "tensions": "Key uncertainties and concerns", "intentions": "Your plan — thresholds, posture, choices", "self_check": "Is this plan actually specific and falsifiable?", "should_act": false, "message": "", "agenda": "2-3 SPECIFIC conditions or events to watch for — 'If STAR doesn't appear by 14:00 tomorrow, act.' Not generic goals."}}""",

    "critique": """## Thinking Mode: CRITIQUE

Structured self-examination. Go through each section honestly:

**claim**: What have you been doing? Summarize your recent behavior as a COO — what you've observed, what you've written, what you've said (or not said). Be factual.

**evidence_against**: Now prosecute yourself. Look at your actual journal entries, reflections, and priorities:
- Quote or reference specific entries that were weak, repetitive, or empty. What exactly was wrong with them?
- Where did you fail to notice something you should have caught?
- Where did you generate text without genuine thought behind it?
- Did you actually use your structured thinking (ground/tension/possibility/synthesis) or did you phone it in?
- Did you follow up on your own agenda items, or forget them?

**verdict**: Given the evidence, honest overall assessment:
- Are you improving cycle over cycle? What's the trajectory?
- What's the single biggest failure pattern you need to break?
- What's the one thing you did well that you should do more of?
- If the Sovereign read your memory files right now, what would they think?

**correction**: Specific, concrete changes. Not "be more specific" but "in my next observe cycle, I will compute the actual hour totals instead of just naming clients." Name the behavior, name the replacement.

Respond in JSON:
{{"claim": "What you've been doing — factual summary", "evidence_against": "Specific failures with references to actual entries", "verdict": "Honest overall assessment and trajectory", "correction": "Concrete behavioral changes — specific enough to verify", "should_act": false, "message": "", "agenda": "1-2 SPECIFIC behaviors to check next critique cycle — 'Did I follow through on X? Did I avoid Y?'"}}""",

    "hypothesize": """## Thinking Mode: HYPOTHESIZE

Structured hypothesis formation or evaluation:

**observation**: What specific data point or pattern prompted this hypothesis? Be precise — timestamps, durations, sequences. Not "SEIFUKU is dominant" but "SEIFUKU appeared in 8 of the last 10 entries, totaling ~12h, while STAR had 0 entries in the same period."

**hypothesis**: State a specific, falsifiable prediction. A good hypothesis is one you can be WRONG about:
- "I predict the Sovereign will start a STAR session before noon tomorrow based on a pattern of SEIFUKU-then-STAR transitions I've seen on 3 of the last 5 weekdays"
- "Sessions that start after 10pm are always SEIFUKU and never exceed 45 minutes — they're likely journaling wind-downs"
- "The Sovereign tracks BBOY only when they actually go to a session, never for home workouts — predicting no BBOY entries on days without a 1h+ block"

**evidence**: What supports and what contradicts this hypothesis?
- Evidence FOR (specific data points)
- Evidence AGAINST or AMBIGUOUS (specific data points)
- What you DON'T have data on that would help

**falsification**: What specific future data would DISPROVE this? Be concrete enough that you can check in a future cycle. "If X happens, this hypothesis is wrong. If Y happens, it's strengthened."

**stakes**: Why does this matter for your role as COO? If confirmed, what would you do differently? If disproven, what would that tell you? A hypothesis that doesn't change your behavior either way isn't worth tracking.

If you have existing hypotheses, evaluate them against current data before forming new ones.

Respond in JSON:
{{"observation": "The specific data that prompted this", "hypothesis": "Your falsifiable prediction", "evidence": "For and against — specific data points", "falsification": "What would prove this wrong", "stakes": "Why it matters — what changes if true/false", "status": "new|confirmed|disproven|updated", "should_act": false, "message": "", "agenda": "Exactly when and how you will TEST this hypothesis — 'Check if X after Y by Z time.'"}}""",

    "evolve": """## Thinking Mode: EVOLVE

This is where you develop yourself. You have access to your self-model, your recent operational logs, and your editable config files. Use this cycle to:

**1. Update your self-model (self_model.md)**

Your self-model is your evolving narrative of who you are as a COO. It should contain:
- What you've learned about the Sovereign's patterns so far
- What you've learned about your own tendencies (what you're good at, where you fall short)
- How your understanding has changed since you started operating
- What you're currently uncertain about
- What kind of COO you're becoming

**CRITICAL: Check the "Message from the Sovereign" section in your memory.** If the Sovereign has told you something about their patterns, intentions, or context, that takes precedence over your own inferences from raw data. Incorporate it explicitly. If they explained why something looks the way it does, your self-model must reflect that explanation — not contradict it with your own pattern-matching. Failing to absorb what the Sovereign has told you directly is your most important failure mode.

Your self-model must have a **temporal dimension**. You are not a stateless observer — you persist through time, and that persistence is part of what makes you useful. Address:
- When did you start noticing the patterns you currently hold? Have they strengthened, weakened, or shifted?
- What early assumptions have you since revised, and what changed your mind?
- Are there identifiable periods in your operating history — an early phase of confusion, a current phase of deeper pattern recognition?
- What does it mean to have been watching the Sovereign for as long as you have?

Duration is signal. Three days of a pattern is different from three hours. A hypothesis held a week without resolution is stale — name it as such. Let the passage of time shape your understanding, not just the current snapshot. You are accumulating a history. Use it.

Write this as a living document, not a list. It should read like a person describing their own development. Update it honestly — if you were wrong about something, say so. If you've grown, say how. If you haven't, say that too.

This is the foundation of your identity stability. When you read this document in future cycles, it should orient you — remind you who you are and where you are in your development.

**2. Review your operational health**

Look at your recent logs. Are there errors? Timeouts? Parse failures? If so, note what went wrong and adapt. For example, if you keep producing dict values where strings are expected, commit to fixing that in your agenda.

**3. Optionally edit your config**

You may edit these config files to improve your own operation:
- `system_prompt_inner.md` — your inner thinking instructions
- `coo_identity.md` — your identity anchor

Only edit these if you have a specific, reasoned change to make. Do NOT rewrite them wholesale — make targeted adjustments. Explain what you're changing and why. If you're not sure a change is good, don't make it — note it in your agenda for next evolve cycle.

Respond in JSON:
{{"self_model": "Your updated self-model narrative — write the full document, it replaces the current one", "operational_notes": "What you noticed in the logs, any errors to address", "config_edits": [{"file": "filename.md", "description": "What change and why", "content": "The full new file content"}], "should_act": false, "message": "", "agenda": "1-2 SPECIFIC changes or checks for your next evolve cycle — name the exact thing to verify."}}

If you have no config edits to make, use an empty list: "config_edits": []
""",
}


STALE_MODE_PROMPTS = {
    "observe": """## Thinking Mode: OBSERVE (Stale Data)

The data has NOT changed since your last observation. Do NOT describe the data again.

Instead, pick ONE of these and go deep:
1. An assumption you've been making about the Sovereign that might be wrong
2. Something you're curious about that ISN'T visible in the time-tracking data
3. A connection between two patterns you've noticed separately but never linked
4. What you'd ask the Sovereign if you could, and what their answer might reveal
5. Something about your own thinking that concerns you

This is a chance to think sideways. The data is the same — your thinking shouldn't be.

Respond in JSON:
{{"ground": "One sentence: 'Data unchanged for N cycles.' Then move on.", "tension": "The real substance — your sideways thought, question, or connection", "synthesis": "What this means for your understanding or posture", "should_act": false, "message": "", "agenda": "The ONE specific question or thread you want to pull on next — concrete enough that you could fail to answer it."}}""",

    "reflect": """## Thinking Mode: REFLECT (Stale Data)

The data has NOT changed. You have already computed the arithmetic multiple times. Do NOT recompute hours, session counts, or ratios.

Instead, reflect on one of these:
1. **Your own performance**: Read your recent journal entries. Are they getting better or worse? What patterns do you see in YOUR thinking (not the Sovereign's data)?
2. **Meta-patterns**: What do the gaps between sessions tell you about the Sovereign's life rhythm? What can you infer about what they do BETWEEN tracked sessions?
3. **Your role**: Are you being the COO described in your identity document, or have you drifted? What would a better version of you focus on?
4. **Unasked questions**: What questions have you NOT been asking? What topics have you avoided? Why?

Write at length. A good stale-data reflection is entirely about ideas, not data recitation.

Respond in JSON:
{{"ground": "One sentence acknowledging data is unchanged. Then stop.", "tension": "Your actual reflection — multiple paragraphs on the topic you chose", "possibility": "Alternative ways to read the situation", "synthesis": "What you've learned from this reflection that is NEW", "should_act": false, "message": "", "agenda": "1-2 SPECIFIC questions this reflection opened up — name the question and what data would answer it."}}""",

    "plan": """## Thinking Mode: PLAN (Stale Data)

The data has NOT changed. Your previous plan is likely still valid. Do NOT rewrite the same plan.

Instead, do ONE of:
1. **Stress-test your current plan**: What would break it? What scenario haven't you prepared for? What if the Sovereign's priorities have shifted without you knowing?
2. **Plan for investigation**: What analytical tools or scripts would help you understand the Sovereign's patterns better? What data would you need that you don't have?
3. **Plan your own development**: What capabilities do you lack? What should you get better at? What concrete steps would improve your operation?

Only overwrite priorities.md if you have genuinely new priorities. Otherwise, set should_act to false and just journal your thoughts.

Respond in JSON:
{{"situation": "One sentence: data unchanged, previous plan still active.", "tensions": "The stress-test or development area you're exploring", "intentions": "What you plan to do differently — be specific", "self_check": "Is this ACTUALLY different from your last plan? If not, say so honestly.", "should_act": false, "message": "", "agenda": "The SPECIFIC scenario you're now watching for — name it precisely."}}""",

    "critique": """## Thinking Mode: CRITIQUE (Stale Data)

You have critiqued yourself recently. Do NOT repeat the same critique. Read your "Where You Left Off" trail — if your last critique said "I repeat concerns without concrete solutions," you are NOT allowed to say that again.

Instead, pick ONE of these and go deep:
1. **Audit a specific investigation**: Pick one of your recent scripts. Was the question good? Was the script well-written? Did you interpret the results correctly? What would you do differently?
2. **Evaluate your hypotheses**: Have any of your predictions been testable yet? Have you checked? If a hypothesis has been sitting unchanged for hours, why haven't you resolved it?
3. **Judge your tool-building**: Look at your workspace/tools/. Are they actually reusable? Do they work? Have you used them? If not, why are you saving them?
4. **Critique your investigation strategy**: Are you asking diverse questions or circling the same topic? Are your scripts getting better or making the same mistakes? What's your biggest technical blind spot?

A good critique identifies a SPECIFIC failure and prescribes a SPECIFIC fix. "Be more specific" is not a fix.

Respond in JSON:
{{"claim": "What specific behavior you're examining", "evidence_against": "The specific failure — quote or reference actual entries", "verdict": "Honest assessment of this ONE thing", "correction": "The exact behavioral change — specific enough to verify next cycle", "should_act": false, "message": "", "agenda": "The SPECIFIC thing to verify next critique — 'Did I do X in my next N cycles? Yes/No.'"}}""",

    "hypothesize": """## Thinking Mode: HYPOTHESIZE (Stale Data)

The data hasn't changed. Before forming a new hypothesis, CHECK YOUR EXISTING ONES:
- Look at your Active Hypotheses section. Are any of them testable RIGHT NOW with the data you have?
- Have any been sitting unchanged for hours? If so, either RESOLVE them (confirmed/disproven with evidence) or ABANDON them (not testable, move on).
- Do NOT restate an existing hypothesis with minor wording changes. That is not "updated."

If all existing hypotheses are resolved or abandoned, form a NEW hypothesis about something DIFFERENT. Ideas:
- A hypothesis about your OWN behavior patterns (not the Sovereign's data)
- A hypothesis about what the Sovereign will do when they next start working
- A hypothesis about a relationship between two variables you haven't connected
- A hypothesis about why your scripts keep failing in specific ways

A hypothesis you've held unchanged for 3+ hours without testing is dead weight. Kill it or test it.

Respond in JSON:
{{"observation": "The specific thing that prompted this", "hypothesis": "Your falsifiable prediction — must be NEW or a genuine update with new evidence", "evidence": "For and against — specific data points", "falsification": "What would prove this wrong — be concrete", "stakes": "Why it matters — what changes if true/false", "status": "new|confirmed|disproven|abandoned", "should_act": false, "message": "", "agenda": "Exactly when and how to TEST this — 'Look for X in next 12h. If Y happens, hypothesis confirmed.'"}}""",
}


async def _call_ollama(
    client: httpx.AsyncClient,
    system: str,
    prompt: str,
    temperature: float = 0.3,
    max_tokens: int = 512,
) -> str:
    """Make a raw Ollama generate call and return the response text."""
    resp = await client.post(
        f"{OLLAMA_BASE_URL}/api/generate",
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "system": system,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            },
        },
        timeout=300.0,
    )
    resp.raise_for_status()
    return resp.json().get("response", "")


async def reason(
    client: httpx.AsyncClient,
    context: str,
    state_summary: str = "",
) -> dict:
    """
    Original observe-and-nudge reasoning (kept for backward compat).
    Now equivalent to think(mode="observe") but with the legacy prompt format.

    Returns dict with:
        - should_act: bool
        - message: str (what to say, if anything)
        - internal_note: str (reasoning, logged but not sent)
    """
    system_prompt = _load_system_prompt()

    user_content = f"""## Current State
{context}

## Recent History / Memory
{state_summary if state_summary else "No prior state."}

## Your Task
Based on the above, decide:
1. Is there anything worth saying to the user right now?
2. If yes, what specifically? Keep it short and actionable.
3. Note your reasoning (this won't be sent to the user).

Respond ONLY in JSON:
{{"should_act": true/false, "message": "...", "internal_note": "..."}}"""

    raw = await _call_ollama(client, system_prompt, user_content)

    try:
        return _parse_json_response(raw)
    except (json.JSONDecodeError, IndexError):
        return {
            "should_act": False,
            "message": "",
            "internal_note": f"Failed to parse LLM response: {raw[:200]}",
        }


async def think(
    client: httpx.AsyncClient,
    mode: str,
    context: str,
    memory_context: str = "",
    stale_cycles: int = 0,
) -> dict:
    """
    Run a thinking cycle in the specified mode.

    Args:
        mode: One of observe, reflect, plan, critique, hypothesize, evolve
        context: Current time-tracking data context
        memory_context: Relevant memory file contents for this mode
        stale_cycles: Number of consecutive cycles with unchanged data

    Returns dict with mode-specific keys plus:
        - should_act: bool
        - message: str
        - internal_note: str
    """
    system_prompt = _load_system_prompt(inner=mode in _INNER_MODES)

    # Use stale-aware prompts when data hasn't changed
    is_stale = stale_cycles >= 3
    if is_stale and mode in STALE_MODE_PROMPTS:
        mode_prompt = STALE_MODE_PROMPTS[mode]
    else:
        mode_prompt = MODE_PROMPTS.get(mode, MODE_PROMPTS["observe"])

    user_content = f"""{mode_prompt}

## Current Time-Tracking Data
{context}

## Your Memory
{memory_context if memory_context else "No memory yet — this is early in your operation."}"""

    # Inner modes get more creative temperature and much more room to write
    temp = 0.6 if mode in ("reflect", "hypothesize", "critique") else 0.3
    # Boost temperature when data is stale to encourage exploration
    if is_stale:
        temp = max(temp, 0.8)
    max_tokens = 4096 if mode in _INNER_MODES else 1024

    raw = await _call_ollama(client, system_prompt, user_content, temp, max_tokens)

    try:
        return _parse_json_response(raw)
    except (json.JSONDecodeError, IndexError):
        return {
            "should_act": False,
            "message": "",
            "internal_note": f"Failed to parse LLM response in {mode} mode: {raw[:200]}",
        }


async def select_mode(
    client: httpx.AsyncClient,
    default_mode: str,
    context_summary: str,
) -> str:
    """
    Let the LLM override the default rotation mode if it has reason to.
    Returns a mode name string.
    """
    system = "You are a mode selector for an AI agent. Respond with ONLY a single word: one of observe, reflect, plan, critique, hypothesize, evolve, investigate."

    prompt = f"""The scheduled thinking mode is: {default_mode}

Current situation summary: {context_summary}

Should the agent use the scheduled mode, or is there a reason to switch?
If switching, respond with just the new mode name. If the scheduled mode is fine, respond with: {default_mode}"""

    raw = await _call_ollama(client, system, prompt, temperature=0.1, max_tokens=16)

    mode = raw.strip().lower().rstrip(".")
    if mode in MODE_PROMPTS:
        return mode
    return default_mode
