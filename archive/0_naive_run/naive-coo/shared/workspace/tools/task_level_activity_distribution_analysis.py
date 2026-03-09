"""Investigation: This script investigates the distribution of task-level activities within each client over the last week and assesses their alignment with the Sovereign's broader objectives. It calculates the mean duration for each task within each client and prints the results, providing insights into potential imbalances or patterns that could inform adjustments to priorities or alert thresholds.
Generated: 20260307_013020 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data for the last week
entries = query_entries(days=7)

# Convert the entries to a DataFrame with proper types
df = entries_to_dataframe(entries)

# Group by client and project, calculate mean duration for each task
task_durations = df.groupby(['client_name', 'project_name'])['duration_seconds'].mean().reset_index()

# Print the results in a clear format
print(task_durations)
