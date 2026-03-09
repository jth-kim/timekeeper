"""Investigation: This script investigates whether the gap after training sessions correlates with the type of session that follows. It specifically tests if training sessions followed by coding sessions (👾 Coding) have shorter gaps than training sessions followed by other session types. This addresses the unexplored question in our agenda about gap patterns by analyzing the next session's content rather than just the training session itself. The findings will determine if the long gaps after training (561.6 min) are due to scheduling patterns (e.g., training followed by coding on the same day) or if they're primarily caused by training sessions being followed by non-coding sessions (like meetings or rest periods) that require longer recovery. This is the first investigation to connect session sequencing with gap duration, moving beyond previous gap analyses that only categorized gaps by session type.
Generated: 20260308_121415 UTC
"""

from supabase_helper import query_entries, entries_to_dataframe
import pandas as pd
from datetime import timedelta

df = entries_to_dataframe(query_entries(days=30))

def has_coding_tag(tags):
    return '👾 Coding' in tags if isinstance(tags, list) else False

# Filter for training sessions with '⚡️ Training' tag
training_sessions = df[df['tags'].apply(lambda x: '⚡️ Training' in (x if isinstance(x, list) else []))]

# Get next session start times for each training session
next_starts = []
for _, row in training_sessions.iterrows():
    # Find next session chronologically (after current session ends)
    next_sessions = df[df['start'] > row['stop']].sort_values('start')
    if not next_sessions.empty:
        next_starts.append(next_sessions.iloc[0]['start'])
    else:
        next_starts.append(pd.NaT)

# Calculate gaps in minutes
training_sessions = training_sessions.copy()
training_sessions['next_start'] = next_starts
training_sessions['gap_minutes'] = training_sessions.apply(
    lambda row: (row['next_start'] - row['stop']).total_seconds() / 60 if pd.notna(row['next_start']) else None,
    axis=1
)

# Identify next session type
training_sessions['next_has_coding'] = training_sessions['next_start'].apply(
    lambda ts: has_coding_tag(df[df['start'] == ts]['tags'].values[0]) if pd.notna(ts) else False
)

# Compute metrics
valid_gaps = training_sessions.dropna(subset=['gap_minutes'])

coding_gaps = valid_gaps[valid_gaps['next_has_coding']]['gap_minutes']
non_coding_gaps = valid_gaps[~valid_gaps['next_has_coding']]['gap_minutes']

# Print results
print("Training sessions followed by coding (👾 Coding):")
if not coding_gaps.empty:
    print(f"  Count: {len(coding_gaps)}")
    print(f"  Avg gap: {coding_gaps.mean():.1f} min (min: {coding_gaps.min():.1f}, max: {coding_gaps.max():.1f})")
else:
    print("  No training sessions followed by coding sessions found")

print("\
Training sessions followed by non-coding sessions:")
if not non_coding_gaps.empty:
    print(f"  Count: {len(non_coding_gaps)}")
    print(f"  Avg gap: {non_coding_gaps.mean():.1f} min (min: {non_coding_gaps.min():.1f}, max: {non_coding_gaps.max():.1f})")
else:
    print("  No training sessions followed by non-coding sessions found")

print(f"\
Overall training average gap: {valid_gaps['gap_minutes'].mean():.1f} min")