"""Investigation: This script investigates the factors contributing to the significant transitions between SEIFUKU and BBOY, analyzing recent time-tracking data. It calculates transition counts between these clients and examines average session lengths for each client to understand their impact on overall time allocation against target priorities.
Generated: 20260305_052503 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query recent entries for analysis
recent_entries = query_entries(days=14)

# Convert to DataFrame for easier manipulation
df = pd.DataFrame(recent_entries)

# Ensure 'client_name' and 'project_name' are correctly typed
df['client_name'] = df['client_name'].astype(str)
df['project_name'] = df['project_name'].astype(str)

# Filter entries related to SEIFUKU and BBOY for transition analysis
seifuku_bboy_entries = df[(df['client_name'] == 'SEIFUKU') | (df['client_name'] == 'BBOY')]

# Calculate transitions between SEIFUKU and BBOY
transitions = seifuku_bboy_entries['client_name'].shift() + ' to ' + seifuku_bboy_entries['client_name']
transition_counts = transitions.value_counts()

# Analyze average session lengths for each client
average_session_lengths = df.groupby('client_name')['duration'].mean()

# Print findings in a clear format
print('Transition Counts:')
print(transition_counts)
print('\
Average Session Lengths by Client:')
print(average_session_lengths)
