"""Investigation: This script investigates the patterns of session lengths for each client across different days of the week, providing insights into how productivity varies across different days and clients.
Generated: 20260307_233314 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data
entries = query_entries(days=14)

# Convert to dataframe
df = entries_to_dataframe(entries)

# Calculate session lengths in seconds
df['session_length_seconds'] = df['duration_seconds']

# Group by client and day of week
grouped_df = df.groupby(['client_name', pd.Grouper(key='start', freq='D')])['session_length_seconds'].mean().reset_index()

# Print results
print(grouped_df)
