"""Investigation: This script investigates the task-level activities within each client that contribute to session length variability and assesses their alignment with the Sovereign's long-term objectives. It calculates the sum of duration seconds for each task within each client, sorts the results in descending order, and prints the top tasks.
Generated: 20260306_095449 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

df = entries_to_dataframe(query_entries(days=14))

task_durations = df.groupby(['client_name', 'project_name'])['duration_seconds'].sum().reset_index()
task_durations = task_durations.sort_values(by='duration_seconds', ascending=False)
print(task_durations)
