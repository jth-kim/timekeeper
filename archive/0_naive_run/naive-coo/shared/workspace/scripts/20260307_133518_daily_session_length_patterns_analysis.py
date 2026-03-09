"""Investigation: This script investigates the daily patterns of session lengths for each client over the last 14 days, providing insights into how productivity varies across different days and clients.
Generated: 20260307_133518 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data
entries = query_entries(days=14)

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Group by client and day of week, calculate mean session length
daily_session_lengths = df.groupby(['client_name', pd.Grouper(key='start', freq='D')])['duration_seconds'].mean().reset_index()

# Print daily session length patterns for each client
print(daily_session_lengths)
