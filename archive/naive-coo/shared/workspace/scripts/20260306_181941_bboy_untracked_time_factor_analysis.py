"""Investigation: This script investigates the factors contributing to the high untracked time for BBOY and assesses their impact on overall time allocation against target priorities.
Generated: 20260306_181941 UTC
"""


import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds

# Query recent entries for BBOY
entries = query_entries(days=14)
bboy_entries = [entry for entry in entries if entry['client_name'] == 'BBOY']

# Convert entries to DataFrame with proper types
df = entries_to_dataframe(bboy_entries)

# Calculate total untracked time for BBOY
untracked_time = df['duration_seconds'].sum()

# Print findings
print(f'Total untracked time for BBOY: {untracked_time} seconds')

# Investigate factors contributing to high untracked time
factors = []
for index, row in df.iterrows():
    if row['duration_seconds'] > 3600:  # More than 1 hour
        factors.append(row)

# Print factors
print('Factors contributing to high untracked time:')
for factor in factors:
    print(factor)
