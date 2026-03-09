"""Investigation: This script investigates the relationship between untracked time and client transitions, aiming to understand how gaps between sessions impact overall time allocation against target priorities. By analyzing recent time-tracking data and calculating mean untracked times for each client, it provides insights into potential imbalances or patterns that could inform adjustments to alert thresholds configuration.
Generated: 20260305_063933 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query recent entries
entries = query_entries(days=14)

# Convert to DataFrame
df = pd.DataFrame(entries)

# Calculate untracked time between sessions
df['start'] = pd.to_datetime(df['start'])
df['stop'] = pd.to_datetime(df['stop'])
df['duration'] = df['stop'] - df['start']
df['untracked_time'] = df['start'].diff()

# Group by client and calculate mean untracked time
mean_untracked_times = df.groupby('client_name')['untracked_time'].mean()

# Print results
print(mean_untracked_times)
