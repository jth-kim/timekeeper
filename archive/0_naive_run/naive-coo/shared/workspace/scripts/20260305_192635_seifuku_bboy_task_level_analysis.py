"""Investigation: This script investigates task-level details for SEIFUKU and BBOY, aiming to understand the factors contributing to differences in session lengths and client transition rates. By analyzing recent entries, calculating average session lengths, and examining project-specific transition rates, this investigation provides insights into how different tasks or projects within each client impact overall time allocation patterns.
Generated: 20260305_192635 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent entries for SEIFUKU and BBOY
entries = query_entries(days=14)
seifuku_entries = [e for e in entries if e['client_name'] == 'SEIFUKU']
bboy_entries = [e for e in entries if e['client_name'] == 'BBOY']

# Convert to DataFrames
seifuku_df = entries_to_dataframe(seifuku_entries)
bboy_df = entries_to_dataframe(bboy_entries)

# Calculate average session lengths and transition rates for each project within SEIFUKU and BBOY
seifuku_project_avg_session_lengths = seifuku_df.groupby('project_name')['duration_seconds'].mean()
bboy_project_avg_session_lengths = bboy_df.groupby('project_name')['duration_seconds'].mean()

print('SEIFUKU Project Average Session Lengths:')
print(seifuku_project_avg_session_lengths)
print('\
BBOY Project Average Session Lengths:')
print(bboy_project_avg_session_lengths)

# Calculate client transition rates for each project within SEIFUKU and BBOY
seifuku_transition_rates = seifuku_df['project_name'].value_counts(normalize=True)
bboy_transition_rates = bboy_df['project_name'].value_counts(normalize=True)

print('\
SEIFUKU Project Transition Rates:')
print(seifuku_transition_rates)
print('\
BBOY Project Transition Rates:')
print(bboy_transition_rates)
