"""Investigation: This script investigates the daily patterns of session lengths for each client over the last 14 days, providing insights into how productivity varies across different days and clients.
Generated: 20260307_103914 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data
entries = query_entries(days=14)

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate session length in seconds for each entry
df['session_length_seconds'] = df['duration_seconds']

# Group by client and day of week, then calculate mean session length
daily_variability = df.groupby(['client_name', pd.Grouper(key='start', freq='D')])['session_length_seconds'].std().reset_index()

# Print the result in a clear format
print(daily_variability)