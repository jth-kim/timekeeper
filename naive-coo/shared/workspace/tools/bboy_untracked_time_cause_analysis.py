"""Investigation: This script calculates the discrepancy between the reported BBOY untracked time and the expected total time based on target allocation, providing insight into potential imbalances in time allocation.
Generated: 20260305_145437 UTC
"""

import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds

df = pd.DataFrame(query_entries(days=14))
# Calculate total tracked time for BBOY
total_tracked_time_bboy = df[df['client_name'] == 'BBOY']['duration'].apply(parse_duration_seconds).sum()
# Calculate expected total time based on target allocation
target_allocation_bboy = 0.2  # Target allocation for BBOY
expected_total_time_bboy = target_allocation_bboy * (14 * 24 * 60 * 60)  # Expected total time in seconds
# Calculate discrepancy
discrepancy = expected_total_time_bboy - total_tracked_time_bboy
print(f'Discrepancy in BBOY\'s untracked time: {discrepancy} seconds')