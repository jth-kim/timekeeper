"""Investigation: This script investigates session length patterns by day of week specifically for SEIFUKU, aiming to understand how productivity varies across different days. It queries recent time-tracking data, filters for SEIFUKU entries, calculates mean session lengths for each day of the week, and prints these averages in a clear format.
Generated: 20260306_120854 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Get recent entries (e.g., last 14 days)
entries = query_entries(days=14)

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Filter for SEIFUKU and other clients if needed
seifuku_df = df[df['client_name'] == 'SEIFUKU']

# Group by day of week and calculate mean session length
session_length_by_day = seifuku_df.groupby(seifuku_df['start'].dt.dayofweek)['duration_seconds'].mean()

# Print results in a clear format
print('Session length patterns for SEIFUKU by day of week:')
print(session_length_by_day)
