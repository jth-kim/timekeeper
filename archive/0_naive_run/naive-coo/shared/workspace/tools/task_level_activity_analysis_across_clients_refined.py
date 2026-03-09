"""Investigation: This script investigates the task-level activities within each client that contribute to session length variability and assesses their impact on overall time allocation against target priorities. It calculates the mean session length for each client, groups tasks by duration, and plots a bar chart of task durations.
Generated: 20260306_031718 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

df = entries_to_dataframe(query_entries(days=30))
# Filter for each client and calculate mean session length
for client in df['client_name'].unique():
    client_df = df[df['client_name'] == client]
    mean_session_length = client_df['duration_seconds'].mean()
    print(f'Mean session length for {client}: {mean_session_length} seconds')
# Group tasks by duration and plot a bar chart of task durations
for client in df['client_name'].unique():
    client_df = df[df['client_name'] == client]
    task_durations = client_df.groupby('description')['duration_seconds'].sum()
    print(f'Task durations for {client}:\n{task_durations}')