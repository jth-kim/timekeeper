"""Investigation: This script investigates the task-level activities within each client that contribute to session length variability and assesses their impact on overall time allocation against target priorities. It calculates the total duration for each task within each client and prints the results in a sorted format, allowing for easy identification of tasks with the longest durations.
Generated: 20260306_062027 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

df = entries_to_dataframe(query_entries(days=30))

task_durations = df.groupby(['client_name', 'project_name'])['duration_seconds'].sum().reset_index()

task_durations = task_durations.sort_values(by='duration_seconds', ascending=False)

print(task_durations)