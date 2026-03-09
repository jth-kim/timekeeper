"""Investigation: This script investigates the relationship between session lengths and client transitions over the last 14 days, aiming to understand how time allocation varies across different clients and projects. It calculates mean session lengths for each client and examines patterns of client transitions to inform adjustments to priorities or alert thresholds.
Generated: 20260306_203701 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

df = entries_to_dataframe(query_entries(days=14))
# Calculate session lengths in seconds and convert to numeric values
df['duration_seconds'] = df['duration'].apply(lambda x: parse_duration_seconds(x))
# Group by client and calculate mean session length
client_session_lengths = df.groupby('client_name')['duration_seconds'].mean()
print(client_session_lengths)
# Investigate patterns of client transitions
transitions = df[['client_name', 'start']]
transitions['next_client'] = transitions['client_name'].shift(-1)
transition_patterns = transitions.groupby(['client_name', 'next_client']).size().reset_index(name='count')
print(transition_patterns)