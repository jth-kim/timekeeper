"""Investigation: This script investigates the patterns of session length variability across different days of the week for each client over the last 14 days, providing insights into how productivity varies across different days and clients.
Generated: 20260307_150054 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data
entries = query_entries(days=14)

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Group by client and day of week, calculate mean session length
session_lengths = df.groupby(['client_name', pd.Grouper(key='start', freq='D')])['duration_seconds'].mean().reset_index()

# Print the results
print(session_lengths)
