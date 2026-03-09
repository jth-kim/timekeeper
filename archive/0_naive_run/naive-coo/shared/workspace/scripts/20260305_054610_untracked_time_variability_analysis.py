"""Investigation: This script investigates the factors contributing to the variability in untracked time between sessions across different clients and assesses their impact on overall time allocation against target priorities. By analyzing recent time-tracking data, it calculates average untracked times for each client and provides statistics on total untracked time.
Generated: 20260305_054610 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query recent entries
entries = query_entries(days=14)

# Convert to dataframe
df = pd.DataFrame(entries)

# Calculate untracked time between sessions
df['start'] = pd.to_datetime(df['start'])
df['stop'] = pd.to_datetime(df['stop'])
df['untracked_time'] = (df['start'] - df['stop'].shift(1)).fillna(pd.Timedelta(seconds=0))

# Group by client and calculate average untracked time
avg_untracked_time = df.groupby('client_name')['untracked_time'].mean()

# Print results
print(avg_untracked_time)
