"""Investigation: This script investigates the daily patterns of session lengths for each client over the last 30 days, providing insights into how productivity varies across different days and clients.
Generated: 20260307_151239 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data for the last 30 days
entries = query_entries(days=30)

# Convert entries to a DataFrame with proper types
df = entries_to_dataframe(entries)

# Group by client and day of week, calculate mean session length
daily_patterns = df.groupby(['client_name', pd.Grouper(key='start', freq='D')])['duration_seconds'].mean().reset_index()

# Print the daily patterns for each client
print(daily_patterns)
