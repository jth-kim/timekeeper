"""Investigation: This script investigates the client transition patterns over the last week and analyzes how these transitions impact overall time allocation against target priorities. It calculates the number of times each client is followed by another client and prints these transition patterns. Additionally, it calculates the total time spent on each client and prints this information.
Generated: 20260306_021230 UTC
"""


import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds

# Query entries for the last week
entries = query_entries(days=7)

# Convert entries to a DataFrame
df = pd.DataFrame(entries)

# Calculate session lengths in seconds
df['duration_seconds'] = df['duration'].apply(parse_duration_seconds)

# Extract client names and project names
clients = df['client_name']
projects = df['project_name']

# Create a dictionary to store transition patterns
transition_patterns = {}

# Iterate over the entries to analyze transitions
for i in range(len(entries) - 1):
    current_client = clients.iloc[i]
    next_client = clients.iloc[i + 1]
    
    # Check if the current client is already in the transition patterns dictionary
    if current_client not in transition_patterns:
        transition_patterns[current_client] = {}
        
    # Check if the next client is already in the current client's transition patterns
    if next_client not in transition_patterns[current_client]:
        transition_patterns[current_client][next_client] = 0
        
    # Increment the count for the current client to next client transition
    transition_patterns[current_client][next_client] += 1

# Print the transition patterns
for client, transitions in transition_patterns.items():
    print(f'Transitions from {client}:')
    for next_client, count in transitions.items():
        print(f'  - {next_client}: {count} times')

# Calculate the total time spent on each client
total_time_per_client = df.groupby('client_name')['duration_seconds'].sum()

# Print the total time spent on each client
print('Total time spent on each client:')
print(total_time_per_client)
