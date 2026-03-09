"""Investigation: This script investigates the task-level activities within each client that contribute to the observed differences in average session lengths. It calculates the mean duration for each task within each client and prints the results, providing insights into how these tasks align with the Sovereign's broader objectives.
Generated: 20260307_021317 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data
entries = query_entries(days=14)

# Convert to DataFrame
df = entries_to_dataframe(entries)

# Group by client and calculate mean session length
mean_session_lengths = df.groupby('client_name')['duration_seconds'].mean()

# Print results
print(mean_session_lengths)

# Investigate task-level activities within each client
for client in df['client_name'].unique():
    client_df = df[df['client_name'] == client]
    tasks = client_df['project_name'].unique()
    
    # Calculate mean duration for each task within the client
    task_durations = client_df.groupby('project_name')['duration_seconds'].mean()
    
    print(f'Task-level activities for {client}:')
    print(task_durations)
