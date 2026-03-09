"""Investigation: This script investigates the gaps between sessions (untracked time) for each client across different days of the week and calculates the mean gap length for each client, providing insights into how these gaps impact overall time allocation.
Generated: 20260307_204433 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query recent entries (last 14 days)
entries = query_entries(days=14)

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate gaps between sessions (untracked time)
df['start'] = pd.to_datetime(df['start'])
df['stop'] = pd.to_datetime(df['stop'])
df.sort_values(by='start', inplace=True)
df['gap'] = (df['start'] - df['stop'].shift(1)).dt.total_seconds()

# Group by client and day of week, calculate mean gap
mean_gaps = df.groupby(['client_name', df['start'].dt.dayofweek])['gap'].mean().reset_index()

# Print results in a clear format
print(mean_gaps)
