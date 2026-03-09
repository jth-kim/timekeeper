"""Investigation: This script analyzes the task-level activities within SEIFUKU to understand what contributes to its high session duration and how these activities align with the Sovereign's broader objectives.
Generated: 20260307_095617 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

tasks = query_entries(days=14)
df = entries_to_dataframe(tasks)
seifuku_df = df[df['client_name'] == 'SEIFUKU']
task_durations = seifuku_df.groupby('description')['duration_seconds'].sum().reset_index()
task_durations.sort_values(by='duration_seconds', ascending=False, inplace=True)
print(task_durations)