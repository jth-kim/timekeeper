"""Investigation: This script investigates session length patterns by day of week for each client over the last 14 days, providing insights into how productivity varies across different days and clients.
Generated: 20260306_145641 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data
entries = query_entries(days=14)

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate session length in seconds and convert to hours for easier comparison
df['session_length_hours'] = df['duration_seconds'] / 3600

# Group by client and day of week, then calculate mean session length
grouped_df = df.groupby(['client_name', df['start'].dt.dayofweek])['session_length_hours'].mean().reset_index()

# Rename columns for clarity
grouped_df.columns = ['Client', 'Day of Week', 'Mean Session Length (hours)']

# Print the result
print(grouped_df)
