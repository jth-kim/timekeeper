"""Investigation: This script investigates the factors contributing to the variability in session lengths across different clients over the last two weeks and assesses their impact on overall time allocation against target priorities. It calculates mean session lengths and standard deviations for each client, providing insights into potential imbalances or patterns that could inform adjustments to priorities or alert thresholds.
Generated: 20260306_151639 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data
entries = query_entries(days=14)

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Group by client and calculate mean session length
mean_session_lengths = df.groupby('client_name')['duration_seconds'].mean()

# Calculate standard deviation of session lengths for each client
std_session_lengths = df.groupby('client_name')['duration_seconds'].std()

# Print results
print('Mean Session Lengths by Client:')
print(mean_session_lengths)
print('
Standard Deviation of Session Lengths by Client:')
print(std_session_lengths)

# Investigate factors contributing to variability in session lengths
for client, group in df.groupby('client_name'):
    print(f'
Session Length Variability for {client}:')
    print(group['duration_seconds'].describe())
