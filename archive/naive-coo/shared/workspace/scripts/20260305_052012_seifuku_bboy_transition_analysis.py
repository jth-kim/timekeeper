"""Investigation: This script investigates the factors contributing to the significant transitions between SEIFUKU and BBOY, and how these transitions impact the overall time allocation strategy. It analyzes recent entries, calculates session lengths, and prints findings on transitions and average session lengths for SEIFUKU and BBOY.
Generated: 20260305_052012 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query recent entries
entries = query_entries(days=14)

# Convert to dataframe
df = pd.DataFrame(entries)

# Ensure 'start' and 'stop' are datetime
df['start'] = pd.to_datetime(df['start'])
df['stop'] = pd.to_datetime(df['stop'])

# Calculate session length
df['session_length'] = (df['stop'] - df['start']).dt.total_seconds() / 60

# Filter for SEIFUKU and BBOY
seifuku_bboy_df = df[(df['client_name'] == 'SEIFUKU') | (df['client_name'] == 'BBOY')]

# Analyze transitions
transitions = []
for index, row in seifuku_bboy_df.iterrows():
    if index > 0:
        prev_row = seifuku_bboy_df.iloc[index - 1]
        if row['client_name'] != prev_row['client_name']:
            transition = {
                'from': prev_row['client_name'],
                'to': row['client_name'],
                'session_length': row['session_length']
            }
            transitions.append(transition)

# Print findings
print('Transitions between SEIFUKU and BBOY:')
for transition in transitions:
    print(f