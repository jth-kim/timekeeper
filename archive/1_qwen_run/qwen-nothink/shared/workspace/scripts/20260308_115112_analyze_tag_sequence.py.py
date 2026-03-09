"""Investigation: This script analyzes session sequence patterns using tag data (previously validated in 2026-03-08 22:39 AEDT). It specifically tests whether training sessions (⚡️ Training) consistently follow coding sessions (👾 Coding) with minimal time gaps – a pattern that would indicate intentional energy management. Previous analysis showed training sessions are both short (45.5 min avg) and infrequent (16 sessions/30d), so this sequence analysis reveals whether they're being deliberately scheduled after deep work. This is the first investigation to examine tag sequences rather than isolated tag metrics or project types, addressing the agenda item about 'managing time vs deep work time' by revealing actual workflow rhythm.
Generated: 20260308_115112 UTC
"""

from supabase_helper import query_entries, entries_to_dataframe
import pandas as pd
from datetime import timedelta

# Fetch last 30 days of entries
entries = query_entries(days=30)
df = entries_to_dataframe(entries)

df = df.sort_values('start').reset_index(drop=True)

df['next_start'] = df['start'].shift(-1)
df['time_gap'] = (df['next_start'] - df['stop']).dt.total_seconds() / 3600  # hours

def extract_tag(tags):
    if isinstance(tags, list):
        return [tag for tag in tags if '⚡️' in tag or '👾' in tag][0] if tags else None
    return None

df['current_tag'] = df['tags'].apply(extract_tag)
df['next_tag'] = df['tags'].shift(-1).apply(extract_tag)

def get_transition_count(df, from_tag, to_tag):
    return df[(df['current_tag'] == from_tag) & (df['next_tag'] == to_tag)].shape[0]

def get_avg_gap(df, from_tag, to_tag):
    gaps = df[(df['current_tag'] == from_tag) & (df['next_tag'] == to_tag)]['time_gap']
    return gaps.mean() if not gaps.empty else None

# Calculate specific transition metrics
coding_to_training_count = get_transition_count(df, '👾 Coding', '⚡️ Training')
coding_to_training_avg_gap = get_avg_gap(df, '👾 Coding', '⚡️ Training')

# Print findings
print('=== TRAINING SESSION SEQUENCE ANALYSIS ===')
print(f'\
Total sessions with valid tags: {df.shape[0]}')
print(f'\
Coding (👾) → Training (⚡️) transitions: {coding_to_training_count} times')

if coding_to_training_count > 0:
    print(f'\
Average time gap between coding and training sessions: {coding_to_training_avg_gap:.1f} hours')
    print(f'\
This is compared to average gap between all consecutive sessions: {df["time_gap"].mean():.1f} hours')
else:
    print('\
No coding → training transitions found')

print(f'\
Top 3 most frequent transitions:')
transitions = df[['current_tag', 'next_tag']].dropna().value_counts().head(3)
for (curr, nxt), count in transitions.items():
    print(f'  {curr} → {nxt}: {count} times')