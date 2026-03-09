"""Investigation: This script investigates the task-level activity patterns within SEIFUKU that contribute to its variable session lengths and high untracked time gaps. By analyzing recent time-tracking data, calculating mean session lengths and untracked time gaps for each task-level activity, and printing the results in a clear format, it provides insights into potential imbalances or patterns in time allocation.
Generated: 20260307_191202 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent entries for SEIFUKU
entries = query_entries(client_name='SEIFUKU', days=14)

# Convert to DataFrame
df = entries_to_dataframe(entries)

# Calculate session lengths and untracked time gaps
df['session_length'] = df['duration_seconds']
df['untracked_time_gap'] = df['start'].diff().fillna(0)

# Group by task-level activity (project_name) and calculate mean session length and untracked time gap
task_level_activity_patterns = df.groupby('project_name')[['session_length', 'untracked_time_gap']].mean()

# Print the results
print(task_level_activity_patterns)
