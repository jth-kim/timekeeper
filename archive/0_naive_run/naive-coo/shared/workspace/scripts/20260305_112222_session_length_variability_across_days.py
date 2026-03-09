"""Investigation: This script investigates the patterns of session length variability across different days of the week for each client over the last 30 days. It calculates the mean session length for each client on each day of the week and prints the results in a clear, readable format.
Generated: 20260305_112222 UTC
"""


import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds

# Query entries for the last 30 days
entries = query_entries(days=30)

# Convert entries to a DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate session length in seconds
df['session_length'] = df['duration_seconds']

# Group by client and day of week, calculate mean session length
grouped_df = df.groupby(['client_name', df['start'].dt.dayofweek])['session_length'].mean().reset_index()

# Print the results
print(grouped_df)
