"""Investigation: This script investigates the gaps between sessions (untracked time) for each client across different days of the week and calculates the mean gap length for each client, providing insights into how these gaps impact overall time allocation. The goal is to understand whether there are patterns in untracked time that could inform adjustments to priorities or alert thresholds.
Generated: 20260307_220224 UTC
"""


import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds

# Query recent entries (last 14 days)
entries = query_entries(days=14)

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate gaps between sessions (untracked time)
df['start'] = pd.to_datetime(df['start'])
df['stop'] = pd.to_datetime(df['stop'])
df['next_start'] = df['start'].shift(-1)
df['gap'] = (df['next_start'] - df['stop']).dt.total_seconds()

# Group by client and day of week, calculate mean gap
gaps_df = df.groupby(['client_name', df['start'].dt.dayofweek])['gap'].mean().reset_index()

# Print results
print(gaps_df)
