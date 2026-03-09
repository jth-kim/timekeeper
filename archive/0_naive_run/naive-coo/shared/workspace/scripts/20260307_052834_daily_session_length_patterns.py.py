"""Investigation: This script investigates the daily patterns of session lengths for each client over the last 14 days, aiming to understand how productivity varies across different days and clients. By analyzing recent time-tracking data and calculating mean session lengths for each client by day, it provides insights into potential imbalances or patterns in time allocation.
Generated: 20260307_052834 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data
entries = query_entries(days=14)

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate session lengths in minutes
df['session_length_minutes'] = df['duration_seconds'] / 60

# Group by client and day of week, then calculate mean session length for each group
daily_patterns = df.groupby(['client_name', pd.Grouper(key='start', freq='D')])['session_length_minutes'].mean().reset_index()

# Print daily patterns for each client
print(daily_patterns)
