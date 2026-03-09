"""Investigation: This script investigates the task-level activities within each client that contribute to session length variability and assesses their impact on overall time allocation against target priorities. It calculates the average session length for each client and examines the patterns of task-level activities to understand their influence on time allocation.
Generated: 20260306_042949 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent entries
entries = query_entries(days=14)

# Convert to dataframe
df = entries_to_dataframe(entries)

# Calculate session length for each entry
df['session_length'] = df['duration_seconds']

# Group by client and calculate average session length
client_avg_session_lengths = df.groupby('client_name')['session_length'].mean()

# Print results
print(client_avg_session_lengths)

# Investigate task-level activities within each client
for client in df['client_name'].unique():
  client_df = df[df['client_name'] == client]
  print(f'Task-level activities for {client}:')
  print(client_df[['project_name', 'tags', 'description', 'session_length']].head())
