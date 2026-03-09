"""Investigation: This script investigates session length variability across different days of the week for each client, aiming to understand how productivity varies and whether there are patterns that could inform adjustments to priorities or alert thresholds.
Generated: 20260307_165102 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data
entries = query_entries(days=14)

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Group by client and day of week, calculate mean session length
grouped_df = df.groupby(['client_name', 'start_dt.dt.dayofweek'])['duration_seconds'].mean().reset_index()

# Print results in a clear format
print(grouped_df.pivot(index='client_name', columns='start_dt.dt.dayofweek', values='duration_seconds'))
