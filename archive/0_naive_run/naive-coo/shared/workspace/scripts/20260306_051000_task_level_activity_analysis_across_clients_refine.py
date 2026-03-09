"""Investigation: This script investigates the task-level activities within each client that contribute to session length variability and assesses their impact on overall time allocation against target priorities. It calculates the mean session length for each client and examines the patterns of task-level activities to understand their influence on time allocation.
Generated: 20260306_051000 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

df = entries_to_dataframe(query_entries(days=14))
# Calculate mean session length for each client and project
mean_session_lengths = df.groupby(['client_name', 'project_name'])['duration_seconds'].mean().reset_index()
print(mean_session_lengths)

task_durations = df.groupby(['client_name', 'tags'])['duration_seconds'].sum().reset_index()
print(task_durations)