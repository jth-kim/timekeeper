"""Investigation: This script investigates the task-level activities within each client that contribute to session length variability and assesses their alignment with the Sovereign's broader objectives. It calculates mean session lengths for each client, providing insights into potential imbalances or patterns that could inform adjustments to priorities or alert thresholds.
Generated: 20260307_082111 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data for the last 14 days
entries = query_entries(days=14)

# Convert entries to a DataFrame with proper types
df = entries_to_dataframe(entries)

# Group by client and calculate mean session length
client_session_lengths = df.groupby('client_name')['duration_seconds'].mean()

# Print the results
print(client_session_lengths)

# Investigate task-level activities within each client
for client in df['client_name'].unique():
    client_df = df[df['client_name'] == client]
    print(f'Task-level activities for {client}:')
    print(client_df['description'].value_counts())
