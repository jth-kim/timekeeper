"""Investigation: This script investigates the daily patterns of session lengths for each client over the last 14 days, aiming to understand how productivity varies across different days and clients. By analyzing recent time-tracking data and calculating mean session lengths for each client by day, it provides insights into potential imbalances or patterns in time allocation.
Generated: 20260307_063222 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data
entries = query_entries(days=14)

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Group by client and day of week, calculate mean session length
mean_session_lengths = df.groupby([pd.Grouper(key='start', freq='D'), 'client_name'])['duration_seconds'].mean().reset_index()

# Print the results in a clear format
print(mean_session_lengths)
