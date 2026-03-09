"""Investigation: This script investigates the relationship between gaps in session start times (untracked time) and subsequent session durations across different clients. It calculates the mean untracked time and subsequent session duration for each client, providing insights into potential patterns or correlations that could inform adjustments to priorities or alert thresholds.
Generated: 20260307_010313 UTC
"""


import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds

# Query recent entries (last 14 days)
entries = query_entries(days=14)

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate gaps in session start times (untracked time)
df['start'] = pd.to_datetime(df['start'])
df['previous_stop'] = df['stop'].shift(1)
df['untracked_time'] = (df['start'] - df['previous_stop']).dt.total_seconds()

# Group by client and calculate mean untracked time and subsequent session duration
grouped_df = df.groupby('client_name')[['untracked_time', 'duration_seconds']].mean().reset_index()

# Print results
print(grouped_df)