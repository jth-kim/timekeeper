"""Investigation: This script calculates the discrepancy between the reported BBOY untracked time and previous findings, providing insight into potential imbalances in time allocation.
Generated: 20260305_150323 UTC
"""


import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds

# Query recent entries for BBOY
entries = query_entries(days=30)
bboy_entries = [entry for entry in entries if entry['client_name'] == 'BBOY']

# Calculate total tracked time for BBOY
total_tracked_time = sum(parse_duration_seconds(entry['duration']) for entry in bboy_entries)

# Calculate expected total time based on target allocation
expected_total_time = 0.2 * 24 * 60 * 60  # 20% of total time, assuming 24 hours/day

# Calculate discrepancy
discrepancy = abs(total_tracked_time - expected_total_time)

print(f'Discrepancy in BBOY\'s untracked time: {discrepancy} seconds')
