"""Investigation: This script analyzes the gaps between sessions, calculating untracked time and relating it to overall time allocation patterns. It aims to provide insight into how the Sovereign spends their time outside of logged sessions, potentially indicating distractions or unnoticed patterns.
Generated: 20260304_220603 UTC
"""

import pandas as pd
from supabase_helper import query_entries, read_memory
df = pd.DataFrame(query_entries(days=30))
# Calculate session start and stop times
df['start'] = pd.to_datetime(df['start'])
df['stop'] = pd.to_datetime(df['stop'])
# Sort entries by start time
df.sort_values(by='start', inplace=True)
# Initialize list to store gaps
untracked_times = []
# Iterate over rows to find gaps between sessions
gaps_df = df[['start', 'stop']]
gaps_df['next_start'] = gaps_df['start'].shift(-1)
gaps_df['gap'] = (gaps_df['next_start'] - gaps_df['stop']).dt.total_seconds() / 3600
# Filter out rows where next_start is NaN (last session)
gaps_df = gaps_df[gaps_df['next_start'].notna()]
print(gaps_df[['start', 'stop', 'next_start', 'gap']])