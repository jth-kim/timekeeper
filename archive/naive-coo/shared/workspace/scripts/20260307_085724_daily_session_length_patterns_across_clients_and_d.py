"""Investigation: This script investigates the daily session length patterns for each client over the last 14 days, providing insights into how productivity varies across different days and clients. By analyzing recent time-tracking data and calculating mean session lengths for each client by day of the week, it offers a nuanced view of time allocation patterns.
Generated: 20260307_085724 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data
entries = query_entries(days=14)

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Group by client and day of week, calculate mean session length
daily_patterns = df.groupby([pd.Grouper(key='start', freq='D'), 'client_name'])['duration_seconds'].mean().reset_index()

# Pivot for easier comparison across days
pivoted = daily_patterns.pivot(index='client_name', columns='start', values='duration_seconds')

# Print the pivoted table
print(pivoted)
