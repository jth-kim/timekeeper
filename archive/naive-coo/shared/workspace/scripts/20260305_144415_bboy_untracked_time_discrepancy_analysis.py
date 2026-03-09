"""Investigation: This script investigates the factors contributing to the discrepancy between the reported BBOY untracked time and previous findings, providing insight into potential imbalances or patterns that could inform adjustments to alert thresholds configuration.
Generated: 20260305_144415 UTC
"""

import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds

df = pd.DataFrame(query_entries(days=14))
# Calculate total tracked time for BBOY
bboy_tracked_time = df[df['client_name'] == 'BBOY']['duration'].apply(parse_duration_seconds).sum()
# Calculate expected total time based on target allocation
expected_bboy_time = 0.2 * (14 * 24 * 60 * 60)  # Assuming 20% of total available time
# Calculate discrepancy between tracked and expected time
bboy_discrepancy = abs(bboy_tracked_time - expected_bboy_time)
print(f'Discrepancy in BBOY untracked time: {bboy_discrepancy} seconds')