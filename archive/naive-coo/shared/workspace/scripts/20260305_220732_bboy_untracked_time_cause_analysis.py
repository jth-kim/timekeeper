"""Investigation: This script investigates the factors contributing to the high untracked time for BBOY and assesses their impact on overall time allocation against target priorities.
Generated: 20260305_220732 UTC
"""

import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds

df = pd.DataFrame(query_entries(days=14))
# Convert 'duration' column to numeric values (seconds)
df['duration_seconds'] = df['duration'].apply(parse_duration_seconds)
# Filter for BBOY entries and calculate total untracked time
total_untracked_time_bboy = df[df['client_name'] == 'BBOY']['duration_seconds'].sum()
print(f'Total untracked time for BBOY: {total_untracked_time_bboy} seconds')