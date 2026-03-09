"""Investigation: This script investigates the relationship between session length variability and task-level activities within each client, providing insights into how these activities impact overall time allocation against target priorities.
Generated: 20260306_232550 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data
entries = query_entries(days=14)

# Convert entries to a DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate session length for each entry
df['session_length'] = df['duration_seconds']

# Group by client and calculate mean session length
mean_session_lengths = df.groupby('client_name')['session_length'].mean()

# Print mean session lengths for each client
print(mean_session_lengths)

# Investigate task-level activities within each client
for client in df['client_name'].unique():
    client_df = df[df['client_name'] == client]
    tasks = client_df['project_name'].unique()
    
    # Calculate total duration for each task within the client
    task_durations = client_df.groupby('project_name')['duration_seconds'].sum()
    
    # Print top tasks contributing to session length variability for the client
    print(f'Top tasks for {client}:')
    print(task_durations.sort_values(ascending=False).head(3))
