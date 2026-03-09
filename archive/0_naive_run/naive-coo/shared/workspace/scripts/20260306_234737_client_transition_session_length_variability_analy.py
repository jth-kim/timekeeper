"""Investigation: This script investigates the relationship between client transition patterns and session length variability across different clients over the last two weeks. It calculates the mean session length for each client, identifies client transitions and their counts, and then computes the mean session length for each client transition. The results provide insights into how client transitions impact session length variability, which can inform adjustments to priorities or alert thresholds.
Generated: 20260306_234737 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data for the last 14 days
entries = query_entries(days=14)

# Convert entries to a DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate session lengths in seconds
df['session_length_seconds'] = df['duration_seconds']

# Group by client and calculate mean session length
mean_session_lengths = df.groupby('client_name')['session_length_seconds'].mean()

# Initialize variables to store client transitions and their counts
client_transitions = {}
transition_counts = {}

# Iterate over the DataFrame rows to find client transitions
for index, row in df.iterrows():
    if index > 0:
        previous_client = df.iloc[index-1]['client_name']
        current_client = row['client_name']
        
        # Check for a transition and update counts accordingly
        transition = (previous_client, current_client)
        if transition in client_transitions:
            client_transitions[transition] += 1
        else:
            client_transitions[transition] = 1

# Calculate the mean session length for each client transition
transition_session_lengths = {}
for transition, count in client_transitions.items():
    previous_client, current_client = transition
    transition_df = df[(df['client_name'] == current_client) & (df.index > df[df['client_name'] == previous_client].index)]
    if not transition_df.empty:
        mean_transition_session_length = transition_df['session_length_seconds'].mean()
        transition_session_lengths[transition] = mean_transition_session_length

# Print the results
print('Mean Session Lengths by Client:')
print(mean_session_lengths)
print('
Client Transitions and Their Counts:')
for transition, count in client_transitions.items():
    print(f'{transition}: {count}')
print('
Mean Session Lengths for Each Client Transition:')
for transition, mean_length in transition_session_lengths.items():
    print(f'{transition}: {mean_length} seconds')
