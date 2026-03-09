"""Investigation: This script investigates the factors contributing to the discrepancy between the reported BBOY untracked time and previous findings, aiming to understand how these factors impact the overall time allocation.
Generated: 20260305_093735 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query recent entries
entries = query_entries(days=30)

# Convert to DataFrame
df = pd.DataFrame(entries)

# Filter for BBOY entries
bboy_df = df[df['client_name'] == 'BBOY']

# Calculate total duration and untracked time for BBOY
total_duration = bboy_df['duration'].sum()
untracked_time = bboy_df['untracked_time'].sum()

# Print findings
print(f'Total duration for BBOY: {total_duration} seconds')
print(f'Untracked time for BBOY: {untracked_time} seconds')

# Investigate discrepancy
if untracked_time == 0:
    print('No untracked time found for BBOY.')
else:
    print('Discrepancy found. Further investigation needed.')
