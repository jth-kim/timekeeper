"""Investigation: This script investigates the cause of the high untracked time for BBOY and its impact on overall time allocation against target priorities. By analyzing recent time-tracking data, it calculates the total untracked time for BBOY and provides statistics on BBOY entries, aiming to understand the factors contributing to this discrepancy.
Generated: 20260307_031104 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query recent entries
entries = query_entries(days=14)

# Convert to DataFrame
df = pd.DataFrame(entries)

# Calculate untracked time for BBOY
bboy_entries = df[df['client_name'] == 'BBOY']
untracked_time = bboy_entries['duration'].apply(parse_duration_seconds).sum()

# Print findings
print(f'Total untracked time for BBOY: {untracked_time} seconds')
print(bboy_entries.describe())
