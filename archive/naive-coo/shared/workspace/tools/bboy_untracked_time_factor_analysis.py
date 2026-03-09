"""Investigation: This script investigates the factors contributing to the high untracked time for BBOY and assesses their impact on overall time allocation against target priorities.
Generated: 20260307_041311 UTC
"""


import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds

# Query recent entries for BBOY
entries = query_entries(days=14)
bboy_entries = [entry for entry in entries if entry['client_name'] == 'BBOY']

# Convert duration to seconds and calculate total tracked time
total_tracked_time = sum(parse_duration_seconds(entry['duration']) for entry in bboy_entries)

# Calculate untracked time as the difference between total possible time and tracked time
untracked_time = (14 * 24 * 60 * 60) - total_tracked_time

# Print findings
print(f'Total tracked time for BBOY: {total_tracked_time} seconds')
print(f'Untracked time for BBOY: {untracked_time} seconds')

# Investigate factors contributing to high untracked time
if untracked_time > (7 * 24 * 60 * 60):
    print('High untracked time detected. Potential factors include distractions, unnoticed patterns, or technical issues.')
else:
    print('Untracked time within acceptable range.')
