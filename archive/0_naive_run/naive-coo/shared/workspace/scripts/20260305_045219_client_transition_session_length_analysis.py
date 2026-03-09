"""Investigation: This script investigates the relationship between client transitions and average session lengths across different days of the week. It calculates the mean session length for each client on each day and counts the number of transitions between each pair of clients.
Generated: 20260305_045219 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query entries for the last 30 days
entries = query_entries(days=30)

# Convert to DataFrame
df = pd.DataFrame(entries)

# Ensure 'start' and 'stop' are datetime
df['start'] = pd.to_datetime(df['start'])
df['stop'] = pd.to_datetime(df['stop'])

# Calculate session length in seconds
df['session_length'] = (df['stop'] - df['start']).dt.total_seconds()

# Group by client and day of week, calculate mean session length
mean_session_lengths = df.groupby([pd.Grouper(key='start', freq='D'), 'client_name'])['session_length'].mean().reset_index()

# Calculate transitions between clients
transitions = []
for i in range(len(df) - 1):
    if df.iloc[i]['client_name'] != df.iloc[i+1]['client_name']:
        transitions.append((df.iloc[i]['client_name'], df.iloc[i+1]['client_name']))

# Count transitions between each pair of clients
transition_counts = {}
for transition in transitions:
    if transition not in transition_counts:
        transition_counts[transition] = 0
    transition_counts[transition] += 1

# Print mean session lengths and transition counts
print(mean_session_lengths)
print(transition_counts)
