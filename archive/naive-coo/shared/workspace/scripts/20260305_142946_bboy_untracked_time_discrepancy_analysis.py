"""Investigation: This script investigates the discrepancy between the reported BBOY untracked time and previous findings, providing insight into potential imbalances in time allocation.
Generated: 20260305_142946 UTC
"""


import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds

# Query recent entries for BBOY
entries = query_entries(days=14, client='BBOY')

# Convert entries to DataFrame
df = pd.DataFrame(entries)

# Calculate total tracked time for BBOY
total_tracked_time = sum(parse_duration_seconds(entry['duration']) for entry in entries)

# Calculate expected total time based on target allocation
expected_total_time = 0.2 * 24 * 60 * 60  # 20% of total time in seconds

# Calculate discrepancy between tracked and expected time
discrepancy = abs(total_tracked_time - expected_total_time)

print(f'Total tracked time for BBOY: {total_tracked_time} seconds')
print(f'Expected total time for BBOY: {expected_total_time} seconds')
print(f'Discrepancy: {discrepancy} seconds')