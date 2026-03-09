"""Investigation: This script investigates the specific task-level activities within SEIFUKU that contribute to its high session length and assesses their impact on overall time allocation against target priorities. It calculates the mean duration for each task description within SEIFUKU over the last 30 days.
Generated: 20260306_025538 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

df = entries_to_dataframe(query_entries(days=30))
seifuku_df = df[df['client_name'] == 'SEIFUKU']
task_durations = seifuku_df.groupby('description')['duration_seconds'].mean()
print(task_durations)
