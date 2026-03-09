"""Investigation: This script investigates the factors contributing to the discrepancy between the reported untracked time for BBOY and previous findings, aiming to understand how these factors impact overall time allocation against target priorities.
Generated: 20260305_223156 UTC
"""


from supabase_helper import query_entries
import pandas as pd

# Query recent entries
entries = query_entries(days=14)

# Convert to DataFrame
df = entries_to_dataframe(entries)

# Filter for BBOY entries
bboy_df = df[df['client_name'] == 'BBOY']

# Calculate total tracked time for BBOY
total_tracked_time_bboy = bboy_df['duration_seconds'].sum()

# Calculate expected total time based on target allocation
expected_total_time_bboy = 0.2 * (14 * 24 * 60 * 60)  # 20% of total time over 14 days

# Calculate discrepancy
discrepancy = expected_total_time_bboy - total_tracked_time_bboy

print(f'Discrepancy in untracked time for BBOY: {discrepancy} seconds')
