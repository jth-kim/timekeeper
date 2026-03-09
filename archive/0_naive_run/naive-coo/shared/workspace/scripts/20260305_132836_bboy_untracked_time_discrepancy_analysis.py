"""Investigation: This script investigates the discrepancy in BBOY's untracked time by calculating the total untracked time and average session length for BBOY over the last 14 days.
Generated: 20260305_132836 UTC
"""


import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds

# Query recent entries for BBOY
entries = query_entries(days=14, client='BBOY')

# Convert entries to DataFrame
df = entries_to_dataframe(entries)

# Calculate total untracked time for BBOY
total_untracked_time = df['untracked_time'].sum()

# Calculate average session length for BBOY
average_session_length = df['duration_seconds'].mean()

# Print findings
print(f'Total untracked time for BBOY: {total_untracked_time} seconds')
print(f'Average session length for BBOY: {average_session_length} seconds')