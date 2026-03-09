"""Investigation: This script investigates the relationship between session lengths and client transitions over the last week, providing insights into how time allocation varies across different clients and projects. It calculates mean session lengths for each client and examines the patterns of client transitions to understand their impact on overall time allocation against target priorities.
Generated: 20260305_192051 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

df = entries_to_dataframe(query_entries(days=7))
print(df.head())
# Calculate session lengths and client transitions
df['session_length'] = df['duration_seconds'] / 3600
client_transitions = df['client_name'].shift() != df['client_name']
df['client_transition'] = client_transitions
# Group by client and calculate mean session length and transition rate
grouped_df = df.groupby('client_name')[['session_length', 'client_transition']].mean()
print(grouped_df)
