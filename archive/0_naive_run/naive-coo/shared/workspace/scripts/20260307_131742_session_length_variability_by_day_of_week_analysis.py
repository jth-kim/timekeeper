"""Investigation: This script investigates the patterns of session length variability across different days of the week for each client over the last 14 days, providing insights into how productivity varies across different days and clients.
Generated: 20260307_131742 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data
entries = query_entries(days=14)

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Group by client and day of week, calculate mean session length
grouped_df = df.groupby([pd.Grouper(key='start', freq='D'), 'client_name'])['duration_seconds'].mean().reset_index()

# Pivot for easier comparison
pivoted_df = grouped_df.pivot(index='start', columns='client_name', values='duration_seconds')

# Print results
print(pivoted_df)
