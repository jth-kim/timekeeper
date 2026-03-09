"""Investigation: This script investigates the task-level activities within SEIFUKU that contribute to its high self-transition rate and dominance in time allocation by analyzing recent time-tracking data and calculating the total duration spent on each task within SEIFUKU.
Generated: 20260306_022910 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

df = entries_to_dataframe(query_entries(days=14))
seifuku_df = df[df['client_name'] == 'SEIFUKU']
task_durations = seifuku_df.groupby('project_name')['duration_seconds'].sum().reset_index()
task_durations.sort_values(by='duration_seconds', ascending=False, inplace=True)
print(task_durations)