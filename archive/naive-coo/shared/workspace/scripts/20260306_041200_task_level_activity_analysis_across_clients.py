"""Investigation: This script investigates the task-level activities within each client that contribute to session length variability and assesses their impact on overall time allocation against target priorities. It calculates the mean session length for each client, groups tasks by duration, and plots a bar chart of task durations.
Generated: 20260306_041200 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data
entries = query_entries(days=30)

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Group by client and calculate mean session length
client_means = df.groupby('client_name')['duration_seconds'].mean()

# Print results
print(client_means)

# Calculate task-level activity durations for each client
task_durations = {}
for client in df['client_name'].unique():
    client_df = df[df['client_name'] == client]
    task_durations[client] = client_df.groupby('description')['duration_seconds'].mean()

# Print task-level activity durations for each client
for client, durations in task_durations.items():
    print(f'Task-level activity durations for {client}:')
    print(durations)
