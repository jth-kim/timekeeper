"""Investigation: This script investigates the factors contributing to the high untracked time for BBOY and its impact on overall time allocation against target priorities. By analyzing recent entries, calculating total untracked time, and average session length for BBOY, it provides insights into potential imbalances or patterns that could inform adjustments to alert thresholds configuration.
Generated: 20260305_130019 UTC
"""


import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds

# Query recent entries
entries = query_entries(days=14)

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Filter for BBOY entries
bboy_df = df[df['client_name'] == 'BBOY']

# Calculate total untracked time for BBOY
total_untracked_time_bboy = bboy_df['untracked_time'].sum()

# Calculate average session length for BBOY
average_session_length_bboy = bboy_df['duration_seconds'].mean()

# Print findings
print(f'Total untracked time for BBOY: {total_untracked_time_bboy} seconds')
print(f'Average session length for BBOY: {average_session_length_bboy} seconds')