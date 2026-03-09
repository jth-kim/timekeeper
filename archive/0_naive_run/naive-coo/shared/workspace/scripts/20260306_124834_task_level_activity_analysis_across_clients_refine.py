"""Investigation: This script investigates the task-level activities within each client that contribute to session length variability and assesses their alignment with the Sovereign's long-term objectives. It calculates the mean duration for each task within specific clients and projects, providing insights into potential areas for optimization in time allocation.
Generated: 20260306_124834 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

df = entries_to_dataframe(query_entries(days=14))
# Filter for specific clients and projects if needed
task_durations = df.groupby(['client_name', 'project_name'])['duration_seconds'].mean().reset_index()
task_durations.sort_values(by='duration_seconds', ascending=False, inplace=True)
print(task_durations)