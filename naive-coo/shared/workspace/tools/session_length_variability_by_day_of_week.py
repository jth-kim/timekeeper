"""Investigation: This script investigates the patterns of session length variability across different days of the week for each client over the last 14 days, providing insights into how productivity varies across different days and clients.
Generated: 20260305_105617 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data
entries = query_entries(days=14)

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Group by client and day of week, calculate mean session length
df['day_of_week'] = df['start'].dt.day_name()
grouped_df = df.groupby(['client_name', 'day_of_week'])['duration_seconds'].mean().reset_index()

# Print results in a clear format
print(grouped_df.to_string(index=False))
