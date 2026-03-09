"""Investigation: This script investigates the factors contributing to the high untracked time for BBOY and its impact on overall time allocation against target priorities.
Generated: 20260305_134821 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent entries for BBOY
entries = query_entries(days=14, client='BBOY')

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate total untracked time and average session length for BBOY
total_untracked_time = df['untracked_time'].sum()
average_session_length = df['duration_seconds'].mean()

print(f'Total untracked time for BBOY: {total_untracked_time} seconds')
print(f'Average session length for BBOY: {average_session_length} seconds')