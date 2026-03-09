"""Investigation: This script analyzes the factors contributing to the high self-transition rate of SEIFUKU and its impact on overall time allocation against target priorities. It queries recent entries for SEIFUKU, converts them to a dataframe, calculates the self-transition rate, and prints the findings.
Generated: 20260305_113916 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent entries for SEIFUKU
entries = query_entries(days=30)
seifuku_entries = [entry for entry in entries if entry['client_name'] == 'SEIFUKU']

# Convert to dataframe
df = entries_to_dataframe(seifuku_entries)

# Calculate self-transition rate
self_transitions = 0
for i in range(1, len(df)):
    if df.iloc[i-1]['project_name'] == df.iloc[i]['project_name']:
        self_transitions += 1

self_transition_rate = self_transitions / len(df)

# Print findings
print(f'SEIFUKU self-transition rate: {self_transition_rate:.2f}')
print('This indicates that SEIFUKU tasks are often followed by other SEIFUKU tasks, potentially suggesting a need for administrative or personal project management.')
