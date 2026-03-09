"""Investigation: This script investigates the task-level activities within each client that contribute to session length variability and assesses their alignment with the Sovereign's long-term objectives. It calculates the sum of duration seconds for each task within each client, sorts the results in descending order, and prints the top tasks.
Generated: 20260306_085636 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data
entries = query_entries(days=14)

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Group tasks by client and project name
grouped_df = df.groupby(['client_name', 'project_name'])

# Calculate the sum of duration seconds for each task
task_durations = grouped_df['duration_seconds'].sum()

# Sort the results in descending order
sorted_task_durations = task_durations.sort_values(ascending=False)

# Print the top tasks
print(sorted_task_durations.head(10))
