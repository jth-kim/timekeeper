"""Investigation: This script investigates the relationship between session lengths and client transitions over the last week, aiming to understand how these patterns impact overall time allocation. It calculates mean session lengths for each client and identifies transitions between clients, providing insights into potential imbalances or optimization opportunities.
Generated: 20260305_083631 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query recent time-tracking data
entries = query_entries(days=7)

# Convert to DataFrame
df = pd.DataFrame(entries)

# Calculate session lengths in seconds
def duration_to_seconds(duration):
    h, m, s = map(int, duration.split(':'))
    return h * 3600 + m * 60 + s

df['duration'] = df['duration'].apply(duration_to_seconds)

# Group by client and calculate mean session length
mean_session_lengths = df.groupby('client_name')['duration'].mean()

# Calculate transitions between clients
transitions = []
for i in range(len(df) - 1):
    if df.iloc[i]['client_name'] != df.iloc[i+1]['client_name']:
        transitions.append((df.iloc[i]['client_name'], df.iloc[i+1]['client_name']))

# Print findings
print('Mean session lengths by client:')
print(mean_session_lengths)
print('Transitions between clients:')
for transition in transitions:
    print(transition)
