"""Investigation: This script investigates the task-level activities within SEIFUKU that contribute to its high average duration and assesses their alignment with the Sovereign's long-term objectives. It queries recent time-tracking data, filters for SEIFUKU entries, groups tasks by project name, calculates the sum of duration seconds for each task, sorts the results in descending order, and prints the top tasks.
Generated: 20260306_084657 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

df = entries_to_dataframe(query_entries(days=30))
df_seifuku = df[df['client_name'] == 'SEIFUKU'].copy()

task_durations = df_seifuku.groupby('project_name')['duration_seconds'].sum().reset_index()
task_durations = task_durations.sort_values(by='duration_seconds', ascending=False)
print(task_durations)