"""Investigation: This script investigates the relationship between client transitions and session lengths, aiming to understand how these transitions impact overall time allocation against target priorities. It calculates average session lengths for sessions with and without client transitions and compares them to identify potential patterns or correlations.
Generated: 20260307_015007 UTC
"""


import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds

# Query recent entries
entries = query_entries(days=14)

# Convert to DataFrame
df = pd.DataFrame(entries)

# Calculate session lengths in seconds
df['session_length'] = df['duration'].apply(parse_duration_seconds)

# Identify sessions with and without client transitions
transitions = []
no_transitions = []

for index, row in df.iterrows():
    if index > 0:
        prev_row = df.iloc[index - 1]
        if row['client_name'] != prev_row['client_name']:
            transitions.append(row)
        else:
            no_transitions.append(row)

# Calculate average session lengths for each group
avg_transition_length = sum([row['session_length'] for row in transitions]) / len(transitions) if transitions else 0
avg_no_transition_length = sum([row['session_length'] for row in no_transitions]) / len(no_transitions) if no_transitions else 0

print(f'Average session length with client transitions: {avg_transition_length} seconds')
print(f'Average session length without client transitions: {avg_no_transition_length} seconds')

# Investigate the cause of the difference
if avg_transition_length < avg_no_transition_length:
    print('Client transitions are associated with shorter session lengths.')
else:
    print('Client transitions are not associated with significantly different session lengths.')


