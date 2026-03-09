"""Investigation: This script investigates client transition patterns to understand how different clients are sequenced in the Sovereign's work schedule and assesses their impact on overall time allocation against target priorities.
Generated: 20260307_055341 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query entries for the last 14 days
entries = query_entries(days=14)

# Convert entries to a DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate session lengths and sort by start time
df['session_length'] = df['stop'] - df['start']
df.sort_values(by='start', inplace=True)

# Initialize lists to track transitions
transitions = []

# Loop through sessions to identify transitions
for i in range(len(df) - 1):
    current_client = df.iloc[i]['client_name']
    next_client = df.iloc[i+1]['client_name']
    transition = (current_client, next_client)
    transitions.append(transition)

# Count the occurrences of each transition
transition_counts = {}
for transition in transitions:
    if transition in transition_counts:
        transition_counts[transition] += 1
    else:
        transition_counts[transition] = 1

# Print the transition counts
for transition, count in transition_counts.items():
    print(f'{transition}: {count}')

# Calculate the percentage of time spent on each client after transitioning from another client
client_time_percentages = {}
for client in df['client_name'].unique():
    total_time = 0
    for i in range(len(df) - 1):
        if df.iloc[i+1]['client_name'] == client:
            total_time += (df.iloc[i+1]['stop'] - df.iloc[i+1]['start']).total_seconds()
    client_time_percentages[client] = (total_time / sum(df['session_length'].dt.total_seconds())) * 100

# Print the client time percentages
for client, percentage in client_time_percentages.items():
    print(f'{client}: {percentage}%')
