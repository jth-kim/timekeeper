"""Investigation: This script analyzes the task-level activities within BBOY and calculates the untracked time between its sessions to understand what contributes to its high untracked time and how these align with the Sovereign's broader objectives.
Generated: 20260307_084504 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data for BBOY
entries = query_entries(days=14)
bboy_entries = [entry for entry in entries if entry['client_name'] == 'BBOY']

# Convert to DataFrame and calculate untracked time between sessions
df = entries_to_dataframe(bboy_entries)

# Calculate session lengths and gaps (untracked time) between sessions
session_lengths = df['duration_seconds']
gaps = []
for i in range(1, len(df)):
    gap = (df.iloc[i]['start'] - df.iloc[i-1]['stop']).total_seconds()
    gaps.append(gap)

# Analyze task-level activities within BBOY's sessions
task_level_activities = {}
for index, row in df.iterrows():
    if row['description'] not in task_level_activities:
        task_level_activities[row['description']] = 0
    task_level_activities[row['description']] += row['duration_seconds']

# Print findings
print('Task-level activities within BBOY:')
for activity, duration in task_level_activities.items():
    print(f'{activity}: {duration} seconds')

print('\
Untracked time between sessions for BBOY:')
for i, gap in enumerate(gaps):
    print(f'Gap {i+1}: {gap} seconds')
