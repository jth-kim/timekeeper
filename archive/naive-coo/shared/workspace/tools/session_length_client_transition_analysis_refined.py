"""Investigation: This script investigates the relationship between session lengths and client transitions over the last week, providing insights into how time allocation varies across different clients and projects. It calculates mean session lengths for each client and examines the patterns of client transitions to understand their impact on overall time allocation against target priorities.
Generated: 20260305_164823 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

df = entries_to_dataframe(query_entries(days=7))
# Calculate session lengths in seconds
session_lengths = df['duration_seconds']
# Group by client and calculate mean session length
mean_session_lengths = session_lengths.groupby(df['client_name']).mean()
print(mean_session_lengths)

client_transitions = pd.DataFrame({'from_client': df['client_name'], 'to_client': df['client_name'].shift(-1)})
client_transitions = client_transitions.dropna()
transition_counts = client_transitions.groupby(['from_client', 'to_client']).size().reset_index(name='count')
print(transition_counts)