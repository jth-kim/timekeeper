"""Investigation: This script investigates the relationship between session lengths and client transitions over the last week, providing insights into how time allocation varies across different clients and projects. It calculates mean session lengths for each client and examines the patterns of client transitions to understand their impact on overall time allocation against target priorities.
Generated: 20260305_181632 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent entries
entries = query_entries(days=7)

# Convert to DataFrame
df = entries_to_dataframe(entries)

# Calculate session lengths and client transitions
df['session_length'] = df['duration_seconds']
client_transitions = df['client_name'].shift() != df['client_name']

# Group by client and calculate mean session length
mean_session_lengths = df.groupby('client_name')['session_length'].mean()

# Print results
print(mean_session_lengths)
print(client_transitions.value_counts())
