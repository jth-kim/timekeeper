"""Investigation: This script investigates the gaps between sessions (untracked time) for each client over the last week and calculates the mean gap length for each client, providing insights into how these gaps impact overall time allocation.
Generated: 20260307_083226 UTC
"""

import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds

df = pd.DataFrame(query_entries(days=7))
# Calculate untracked time between sessions
df['start'] = pd.to_datetime(df['start'])
df['stop'] = pd.to_datetime(df['stop'])
df.sort_values(by='start', inplace=True)
df['untracked_time'] = (df['start'] - df['stop'].shift(1)).dt.total_seconds()
df.fillna(0, inplace=True)
# Group by client and calculate mean untracked time
groups = df.groupby('client_name')['untracked_time']
mean_untracked_times = groups.mean().reset_index()
print(mean_untracked_times)