"""Investigation: This script investigates the task-level activity patterns within SEIFUKU that contribute to its variable session lengths across different days of the week. It calculates the total duration for each project within SEIFUKU and prints the results in a sorted format, allowing for easy identification of tasks with the longest durations.
Generated: 20260307_163221 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

df = entries_to_dataframe(query_entries(days=14))
seifuku_df = df[df['client_name'] == 'SEIFUKU']
task_durations = seifuku_df.groupby('project_name')['duration_seconds'].sum().reset_index()
task_durations.sort_values(by='duration_seconds', ascending=False, inplace=True)
print(task_durations)