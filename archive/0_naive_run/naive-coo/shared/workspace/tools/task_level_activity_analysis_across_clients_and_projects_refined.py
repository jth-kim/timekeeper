"""Investigation: This script investigates the task-level activities within each client that contribute to session length variability and assesses their impact on overall time allocation against target priorities. It calculates the mean duration for each task within each client, providing insights into how these tasks align with the Sovereign's priorities and goals.
Generated: 20260306_224523 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data
entries = query_entries(days=30)

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Group by client and project, calculate mean session duration for each task
task_durations = df.groupby(['client_name', 'project_name'])['duration_seconds'].mean().reset_index()

# Sort by mean duration in descending order
task_durations = task_durations.sort_values(by='duration_seconds', ascending=False)

# Print the top tasks with the longest average durations for each client
for client in task_durations['client_name'].unique():
    client_tasks = task_durations[task_durations['client_name'] == client]
    print(f'Top tasks for {client}:')
    print(client_tasks.head(5))
    print('---')
