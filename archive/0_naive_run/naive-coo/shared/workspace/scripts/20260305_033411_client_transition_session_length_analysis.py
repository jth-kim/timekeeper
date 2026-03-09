"""Investigation: This script analyzes the relationship between client transitions and session lengths, providing insights into how these factors impact overall time allocation. By calculating average session lengths for each client and examining client transitions, we can identify potential imbalances in time allocation and inform adjustments to the alert thresholds configuration.
Generated: 20260305_033411 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query recent entries
entries = query_entries(days=30)

# Convert to DataFrame
df = pd.DataFrame(entries)

# Calculate session lengths
df['session_length'] = df['stop'] - df['start']

# Group by client and calculate average session length
avg_session_lengths = df.groupby('client_name')['session_length'].mean()

# Calculate client transitions
transitions = {}
for index, row in df.iterrows():
    if row['client_name'] not in transitions:
        transitions[row['client_name']] = {}
    if row['project_name'] not in transitions[row['client_name']]:
        transitions[row['client_name']][row['project_name']] = 0
    transitions[row['client_name']][row['project_name']] += 1

# Print results
print('Average session lengths by client:')
print(avg_session_lengths)
print('Client transitions:')
print(transitions)
