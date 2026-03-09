"""Investigation: This script investigates the factors contributing to the variability in session lengths across different days of the week for each client over the last 14 days. By analyzing recent time-tracking data and calculating mean session lengths for each client by day of week, it provides insights into how productivity varies across different days and clients.
Generated: 20260307_051039 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data
entries = query_entries(days=14)

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Group by client and day of week, calculate mean session length
session_lengths = df.groupby(['client_name', pd.Grouper(key='start', freq='D')])['duration_seconds'].mean().reset_index()

# Print results
print(session_lengths)
