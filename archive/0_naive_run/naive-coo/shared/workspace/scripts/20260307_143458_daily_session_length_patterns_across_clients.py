"""Investigation: This script investigates the daily patterns of session lengths for each client over the last 30 days, providing insights into how productivity varies across different days and clients.
Generated: 20260307_143458 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data
entries = query_entries(days=30)

# Convert entries to a DataFrame with proper types
df = entries_to_dataframe(entries)

# Group by client and calculate mean session length for each day of the week
daily_session_lengths = df.groupby(['client_name', pd.Grouper(key='start', freq='D')])['duration_seconds'].mean().reset_index()

# Print daily session lengths in a clear format
print(daily_session_lengths)
