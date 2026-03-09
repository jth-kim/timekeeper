"""Investigation: This script investigates the relationship between client transitions and session lengths, aiming to understand how time allocation varies across different clients and projects. It calculates mean session lengths for each client and examines the patterns of client transitions to understand their impact on overall time allocation against target priorities.
Generated: 20260306_093750 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data
entries = query_entries(days=14)

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate session length in seconds
df['session_length_seconds'] = df['duration_seconds']

# Group by client name and project name, calculate mean session length
client_session_lengths = df.groupby(['client_name', 'project_name'])['session_length_seconds'].mean().reset_index()

# Print results
print(client_session_lengths)

# Investigate client transitions
transitions = []
for i in range(len(df) - 1):
    transition = {
        'from_client': df.iloc[i]['client_name'],
        'to_client': df.iloc[i+1]['client_name'],
        'session_length_seconds': df.iloc[i]['session_length_seconds']
    }
    transitions.append(transition)

# Convert transitions to DataFrame
transitions_df = pd.DataFrame(transitions)

# Group by from_client and to_client, calculate mean session length
transition_session_lengths = transitions_df.groupby(['from_client', 'to_client'])['session_length_seconds'].mean().reset_index()

# Print results
print(transition_session_lengths)
