"""Investigation: This script investigates the factors contributing to the high untracked time for BBOY and assesses its impact on overall time allocation against target priorities.
Generated: 20260306_020720 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query recent entries for BBOY
entries = query_entries(days=30)
bboy_entries = [entry for entry in entries if entry['client_name'] == 'BBOY']

# Calculate total tracked time for BBOY
total_tracked_time = sum(parse_duration_seconds(entry['duration']) for entry in bboy_entries)

# Calculate expected total time based on target allocation
expected_total_time = 0.2 * 30 * 24 * 60 * 60  # 20% of total time over 30 days

# Calculate untracked time
untracked_time = expected_total_time - total_tracked_time

print(f'Total tracked time for BBOY: {total_tracked_time} seconds')
print(f'Expected total time for BBOY: {expected_total_time} seconds')
print(f'Untracked time for BBOY: {untracked_time} seconds')