"""Investigation: This script investigates the factors contributing to the variability in untracked time between sessions and assesses their impact on overall time allocation against target priorities. It calculates the mean untracked time for each client, providing insights into potential imbalances or patterns that could inform adjustments to alert thresholds configuration.
Generated: 20260305_202902 UTC
"""


import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds

# Query recent entries
entries = query_entries(days=14)

# Convert to DataFrame with proper types
df = pd.DataFrame(entries)
df['start'] = pd.to_datetime(df['start'])
df['stop'] = pd.to_datetime(df['stop'])

# Calculate session duration in seconds
df['duration_seconds'] = df['duration'].apply(parse_duration_seconds)

# Sort by start time and calculate untracked time between sessions
df.sort_values(by='start', inplace=True)
df['untracked_time'] = (df['start'] - df['stop'].shift(1)).dt.total_seconds()

# Group by client and calculate mean untracked time
mean_untracked_time = df.groupby('client_name')['untracked_time'].mean()

# Print results
print(mean_untracked_time)
