"""Investigation: This script investigates the relationship between session lengths and day of the week for each client over the last 14 days, providing insights into potential patterns or correlations that could inform adjustments to priorities or alert thresholds.
Generated: 20260307_012033 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data
entries = query_entries(days=14)

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Group by client and day of week, calculate mean session length
grouped_df = df.groupby(['client_name', pd.Grouper(key='start', freq='D')])['duration_seconds'].mean().reset_index()

# Print results in a clear format
print(grouped_df.to_string(index=False))