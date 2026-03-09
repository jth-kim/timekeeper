"""Investigation: This script investigates the task-level activities within each client that contribute to session length variability and assesses their alignment with the Sovereign's long-term objectives. It calculates the mean duration for each task within specific clients and projects, providing insights into potential areas for optimization in time allocation.
Generated: 20260306_121633 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

df = entries_to_dataframe(query_entries(days=14))
# Filter for specific clients and projects to analyze task-level activities
client_project_df = df[(df['client_name'] == 'SEIFUKU') | (df['client_name'] == 'STAR')]
client_project_df = client_project_df[client_project_df['project_name'].isin(['Self authoring', 'Time Series'])]

task_durations = client_project_df.groupby('description')['duration_seconds'].mean().reset_index()
task_durations = task_durations.sort_values(by='duration_seconds', ascending=False)
print(task_durations)
