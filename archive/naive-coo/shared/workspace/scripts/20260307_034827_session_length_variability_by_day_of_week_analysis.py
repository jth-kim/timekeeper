"""Investigation: This script investigates the patterns of session length variability across different days of the week for each client and assesses their impact on overall time allocation against target priorities. It calculates mean session lengths for each client by day of week, providing insights into how productivity varies across different days and clients.
Generated: 20260307_034827 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data
entries = query_entries(days=14)

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate session lengths in seconds
df['session_length_seconds'] = df['duration_seconds']

# Group by client and day of week, calculate mean session length
grouped_df = df.groupby(['client_name', df['start'].dt.dayofweek])['session_length_seconds'].mean().reset_index()

# Print results
print(grouped_df)

# Save to file for further analysis
grouped_df.to_csv('/data/workspace/results/session_length_variability_by_day_of_week.csv', index=False)
