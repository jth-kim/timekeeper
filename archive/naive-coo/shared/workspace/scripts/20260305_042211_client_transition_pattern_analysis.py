"""Investigation: This script investigates the patterns of client transitions between sessions over the last week to understand how different clients are sequenced in the Sovereign's work schedule. It also calculates mean session lengths for each client and project to identify potential imbalances in time allocation.
Generated: 20260305_042211 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query entries for the last week
entries = query_entries(days=7)

# Convert to dataframe
df = pd.DataFrame(entries)

# Ensure 'start' and 'stop' columns are datetime
df['start'] = pd.to_datetime(df['start'])
df['stop'] = pd.to_datetime(df['stop'])

# Calculate session length in seconds
df['session_length'] = (df['stop'] - df['start']).dt.total_seconds()

# Group by client name and project name, then calculate mean session length
client_project_session_lengths = df.groupby(['client_name', 'project_name'])['session_length'].mean().reset_index()

# Analyze client transitions
client_transitions = []
for i in range(len(df) - 1):
    current_client = df.iloc[i]['client_name']
    next_client = df.iloc[i+1]['client_name']
    if current_client != next_client:
        client_transitions.append((current_client, next_client))

# Count transitions between clients
transition_counts = {}
for transition in client_transitions:
    if transition in transition_counts:
        transition_counts[transition] += 1
    else:
        transition_counts[transition] = 1

# Print findings
print('Client Transition Patterns:')
for transition, count in transition_counts.items():
    print(f'{transition[0]} -> {transition[1]}: {count} times')

print('\
Mean Session Lengths by Client and Project:')
print(client_project_session_lengths)
