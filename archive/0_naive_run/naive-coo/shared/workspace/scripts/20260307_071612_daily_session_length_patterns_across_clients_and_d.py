"""Investigation: This script investigates the daily patterns of session lengths for each client over the last 14 days, providing insights into how productivity varies across different days and clients. By analyzing recent time-tracking data and calculating mean session lengths for each client by day, it offers a nuanced understanding of time allocation patterns.
Generated: 20260307_071612 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data for the last 14 days
entries = query_entries(days=14)

# Convert entries to a pandas DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate session lengths in minutes and group by client and day of week
df['session_length_minutes'] = df['duration_seconds'] / 60
grouped_df = df.groupby(['client_name', pd.Grouper(key='start', freq='D')])['session_length_minutes'].mean().reset_index()

# Pivot the DataFrame for easier comparison across days
pivoted_df = grouped_df.pivot(index='client_name', columns='start', values='session_length_minutes')

# Print the pivoted DataFrame to see daily patterns of session lengths
print(pivoted_df)
