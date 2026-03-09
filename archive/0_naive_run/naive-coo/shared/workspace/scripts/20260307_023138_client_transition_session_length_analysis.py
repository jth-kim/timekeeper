"""Investigation: This script investigates the relationship between client transitions and session lengths across different clients over the last week. It calculates mean session lengths for each client and analyzes client transitions to understand their impact on overall time allocation against target priorities.
Generated: 20260307_023138 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query recent entries
entries = query_entries(days=7)

# Convert to DataFrame with proper types
df = pd.DataFrame(entries)
df['start'] = pd.to_datetime(df['start'])
df['stop'] = pd.to_datetime(df['stop'])

# Calculate session lengths in seconds
df['duration_seconds'] = (df['stop'] - df['start']).dt.total_seconds()

# Group by client and calculate mean session length
client_session_lengths = df.groupby('client_name')['duration_seconds'].mean()

# Analyze client transitions
transitions = []
for i in range(len(df) - 1):
    current_client = df.iloc[i]['client_name']
    next_client = df.iloc[i+1]['client_name']
    if current_client != next_client:
        transition = {
            'from': current_client,
            'to': next_client,
            'session_length': df.iloc[i]['duration_seconds']
        }
        transitions.append(transition)

# Convert transitions to DataFrame
transitions_df = pd.DataFrame(transitions)

# Group by transition type and calculate mean session length
transition_session_lengths = transitions_df.groupby(['from', 'to'])['session_length'].mean()

# Print findings
print('Client Session Lengths:')
print(client_session_lengths)
print('\
Transition Session Lengths:')
print(transition_session_lengths)
