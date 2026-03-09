"""Investigation: This script investigates the primary factors contributing to session length variability across different days of the week for each client and assesses their impact on overall productivity. By analyzing recent time-tracking data, calculating mean session lengths for each client by day of the week, and printing the results in a clear format, it provides insights into potential imbalances or patterns that could inform adjustments to priorities or alert thresholds.
Generated: 20260307_155614 UTC
"""


import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds

# Query recent entries (e.g., last 14 days)
entries = query_entries(days=14)

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate session length in seconds for each entry
df['session_length_seconds'] = df['duration'].apply(parse_duration_seconds)

# Group by client and day of week, calculate mean session length
grouped_df = df.groupby(['client_name', pd.Grouper(key='start', freq='D')])['session_length_seconds'].mean().reset_index()

# Pivot to compare days of the week easily
pivoted_df = grouped_df.pivot(index='client_name', columns='start', values='session_length_seconds')

# Print pivoted DataFrame for easy comparison
print(pivoted_df)
