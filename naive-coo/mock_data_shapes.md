# Mock Data Shapes

Reference snippets from real files to guide mock data generation.

---

## coo.jsonl

One JSON object per line. Key event types with their distinct shapes:

### Lifecycle events
```jsonl
{"interval_seconds": 1800, "model": "llama3.3:70b", "signal_enabled": false, "event": "coo.starting", "timestamp": "2026-03-04T04:20:08.517722Z", "level": "info"}
{"seconds": 1800, "event": "coo.sleeping", "timestamp": "2026-03-04T04:20:10.019635Z", "level": "info"}
```

### Cycle events
```jsonl
{"last_check": null, "event": "cycle.start", "timestamp": "2026-03-04T04:20:08.592876Z", "level": "info"}
{"event": "cycle.fetch", "timestamp": "2026-03-04T08:10:47.409296Z", "level": "info"}
{"event": "cycle.complete", "timestamp": "2026-03-04T07:44:23.994386Z", "level": "info"}
```

### Error events
```jsonl
{"error": "Client error '400 Bad Request' for url '...'", "error_type": "HTTPStatusError", "event": "cycle.error", "timestamp": "2026-03-04T04:20:10.018720Z", "level": "error"}
```

### Thought events (vary by mode: observe, reflect, plan, critique, investigate, hypothesize)
```jsonl
{"mode": "observe", "cycle": 0, "scheduled": "observe", "event": "cycle.think", "timestamp": "2026-03-04T08:10:55.762254Z", "level": "info"}
{"mode": "observe", "observation": "The user is currently tracking time under SEIFUKU for Self authoring with a coding tag.", "should_act": false, "internal_note": "No immediate need to alert the user.", "event": "cycle.thought", "timestamp": "2026-03-04T08:11:24.346884Z", "level": "info"}
{"mode": "reflect", "reflection": "The user has been consistently tracking time under SEIFUKU...", "should_act": false, "internal_note": "Noted consistent SEIFUKU focus; will continue to monitor for balance.", "event": "cycle.thought", "timestamp": "2026-03-04T08:24:48.301674Z", "level": "info"}
{"mode": "plan", "priorities": "Monitor SEIFUKU activity. Watch for potential neglect of STAR and BBOY.", "should_act": false, "internal_note": "Updated priorities based on recent consistent SEIFUKU activity.", "event": "cycle.thought", "timestamp": "2026-03-04T08:28:15.297735Z", "level": "info"}
{"mode": "critique", "critique": "Recent observations have been accurate... However, there's a risk of neglecting other clients.", "should_act": false, "internal_note": "Continue to monitor while keeping a watchful eye on STAR and BBOY.", "event": "cycle.thought", "timestamp": "2026-03-04T08:42:12.961482Z", "level": "info"}
```

### Context event (contains the full tracking snapshot)
```jsonl
{"context": "Currently tracking: Self authoring\nClient: SEIFUKU\nTags: Coding\nStarted: 2026-03-04T04:01:15+00:00\nElapsed: ~5 minutes\n\nRecent entries (8 in last 48h):\n  2026-03-04T05:18:26+00:00 | SEIFUKU / Artemis [Managing] | -492389:18:26\n  2026-03-04T04:01:15+00:00 | SEIFUKU / Self authoring [Coding] | 00:31:06\n  ...\n\nAlert thresholds config: {\"goal_neglect\": {...}, \"allocation\": {...}, \"anomaly\": {...}, \"cadence\": {...}}", "event": "cycle.context", "timestamp": "2026-03-04T07:44:02.852962Z", "level": "info"}
```

### Judgment event (older format, pre-think-modes)
```jsonl
{"should_act": false, "message": "", "internal_note": "No anomalies or misalignments detected.", "event": "cycle.judgment", "timestamp": "2026-03-04T07:44:23.990515Z", "level": "info"}
```

---

## journal.md

Entries separated by `<!-- entry -->`. Each entry has a heading with UTC timestamp, a mode tag in brackets, and structured sections that vary by mode.

```markdown
### 2026-03-04 21:46 UTC

[critique]

**Claim**: I have been monitoring the user's time-tracking data, analyzing their
recent focus on SEIFUKU...

**Evidence Against**: Upon reviewing my journal entries, I notice that while I
have identified the dominance of SEIFUKU and the absence of STAR activity, my
reflections could delve deeper...

**Verdict**: My overall assessment is that while I have been diligent in
monitoring client activity and identifying areas of concern...

**Correction**: In my next reflection cycle, I will focus on providing more
detailed analyses...
<!-- entry -->
```

---

## self_model.md

Currently empty. Expected to contain self-reflective narrative updated over time.

---

## coo_state.json

```json
{
  "last_check_utc": "2026-03-05T01:34:37.741971+00:00",
  "last_nudge_utc": "2026-03-04T20:33:36.462360+00:00",
  "conversation_summary": "",
  "alert_history": [
    {
      "time": "2026-03-04T21:46:57.299896+00:00",
      "mode": "critique",
      "should_act": false,
      "note": ""
    },
    {
      "time": "2026-03-04T21:49:25.874589+00:00",
      "mode": "investigate",
      "should_act": false,
      "note": ""
    }
  ],
  "last_think_mode": "investigate",
  "cycle_count": 5,
  "data_fingerprint": "1a09fcf63ffd4004",
  "fingerprint_unchanged_cycles": 18
}
```

---

## workspace/scripts/ (analysis script shape)

No `results/` directory exists yet. Scripts live in `workspace/scripts/` and produce stdout output. Representative example:

```python
"""Investigation: Time distribution analysis
Generated: 20260304_215126 UTC
"""

import pandas as pd
from supabase_helper import query_entries

entries = query_entries(days=7)
df = pd.DataFrame(entries)

client_times = df.groupby('client_name')['duration'].sum()
total_time = client_times.sum()
client_percentages = (client_times / total_time) * 100

print(client_percentages)

target_allocations = {'STAR': 0.55, 'BBOY': 0.2, 'SEIFUKU': 0.15, 'BOJ': 0.1}
for client, target in target_allocations.items():
    if client in client_percentages:
        print(f'{client}: {client_percentages[client]}% (target: {target*100}%)')
```

Expected output shape (DataFrame printed to stdout):
```
client_name
BBOY       12.3
BOJ         0.0
SEIFUKU    67.8
STAR       19.9
Name: duration, dtype: float64
```
