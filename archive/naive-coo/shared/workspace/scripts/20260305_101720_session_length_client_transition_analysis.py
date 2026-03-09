"""Investigation: This script investigates the relationship between session lengths and client transitions to understand how time allocation varies across different clients and projects, providing insights into potential imbalances or patterns that could inform adjustments to priorities or alert thresholds.
Generated: 20260305_101720 UTC
"""


import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds

# Query recent entries
entries = query_entries(days=14)

# Convert to DataFrame with proper types
df = pd.DataFrame(entries)
df['start'] = pd.to_datetime(df['start'])
df['stop'] = pd.to_datetime(df['stop'])

# Calculate session length in seconds
df['session_length_seconds'] = (df['stop'] - df['start']).dt.total_seconds()

# Group by client and calculate mean session length
mean_session_lengths = df.groupby('client_name')['session_length_seconds'].mean()

# Investigate client transitions
transitions = []
for i in range(len(entries) - 1):
    transition = {
        'from_client': entries[i]['client_name'],
        'to_client': entries[i+1]['client_name'],
        'session_length_seconds': parse_duration_seconds(entries[i]['duration'])
    }
    transitions.append(transition)

# Convert transitions to DataFrame
transitions_df = pd.DataFrame(transitions)

# Group by from_client and to_client, calculate mean session length for each transition
mean_transition_session_lengths = transitions_df.groupby(['from_client', 'to_client'])['session_length_seconds'].mean()

# Print findings
print('Mean session lengths by client:')
print(mean_session_lengths)
print('\
Mean session lengths by client transition:')
print(mean_transition_session_lengths)
