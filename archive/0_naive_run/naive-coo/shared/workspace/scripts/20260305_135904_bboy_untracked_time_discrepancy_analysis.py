"""Investigation: This script investigates the factors contributing to the discrepancy in BBOY's untracked time by calculating the total tracked time for BBOY, the expected total time based on target allocation, and the discrepancy between these two values.
Generated: 20260305_135904 UTC
"""


import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds

# Query recent entries for BBOY
entries = query_entries(days=14, client='BBOY')

# Convert to DataFrame
df = pd.DataFrame(entries)

# Calculate total tracked time for BBOY
total_tracked_time = sum(parse_duration_seconds(entry['duration']) for entry in entries)

# Calculate expected total time based on target allocation
expected_total_time = 0.2 * (14 * 24 * 60 * 60)  # 20% of total available time over 14 days

# Calculate discrepancy
discrepancy = expected_total_time - total_tracked_time

print(f'Discrepancy in BBOY\'s untracked time: {discrepancy} seconds')
