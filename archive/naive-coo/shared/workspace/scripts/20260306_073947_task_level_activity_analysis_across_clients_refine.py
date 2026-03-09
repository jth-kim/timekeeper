"""Investigation: This script investigates the task-level activities within each client that contribute to session length variability and assesses their impact on overall time allocation against target priorities. It calculates the mean duration for each task within each client and prints the results in a sorted format, allowing for easy identification of tasks with the longest durations.
Generated: 20260306_073947 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data
entries = query_entries(days=14)

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Group by client and project, calculate mean session length
grouped_df = df.groupby(['client_name', 'project_name'])['duration_seconds'].mean().reset_index()

# Print results in a sorted format
print(grouped_df.sort_values(by='duration_seconds', ascending=False))