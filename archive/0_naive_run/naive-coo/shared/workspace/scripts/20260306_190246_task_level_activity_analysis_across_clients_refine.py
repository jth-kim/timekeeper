"""Investigation: This script investigates the task-level activities within each client that contribute to session length variability and assesses their alignment with the Sovereign's objectives. It calculates the mean duration for each task within each client, providing insights into potential imbalances or patterns in time allocation.
Generated: 20260306_190246 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

df = entries_to_dataframe(query_entries(days=14))
print(df.head())
# Calculate session length variability for each client
client_session_lengths = df.groupby('client_name')['duration_seconds'].std()
print(client_session_lengths)
# Identify task-level activities contributing to session length variability within each client
for client, group in df.groupby('client_name'):
    print(f'Client: {client}')
    task_durations = group.groupby('project_name')['duration_seconds'].mean()
    print(task_durations)