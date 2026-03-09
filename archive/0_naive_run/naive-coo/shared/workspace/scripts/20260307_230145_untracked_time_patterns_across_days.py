"""Investigation: This script investigates the patterns of gaps between sessions (untracked time) across different days of the week for each client, aiming to understand how these patterns impact overall time allocation against target priorities. By analyzing recent time-tracking data and calculating mean gap lengths for each client by day of the week, it provides insights into potential imbalances or patterns that could inform adjustments to alert thresholds configuration.
Generated: 20260307_230145 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query recent entries (e.g., last 14 days)
entries = query_entries(days=14)

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate gaps between sessions (untracked time)
df['start'] = pd.to_datetime(df['start'])
df['stop'] = pd.to_datetime(df['stop'])
df['next_start'] = df['start'].shift(-1)
df['gap_seconds'] = (df['next_start'] - df['stop']).dt.total_seconds()

# Group by client and day of week, calculate mean gap length
gaps_df = df.groupby(['client_name', df['start'].dt.dayofweek])['gap_seconds'].mean().reset_index()

# Print results in a clear format
print(gaps_df.pivot(index='client_name', columns='start', values='gap_seconds'))
