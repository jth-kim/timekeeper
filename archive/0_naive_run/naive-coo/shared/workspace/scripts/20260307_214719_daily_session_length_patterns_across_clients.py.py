"""Investigation: This script investigates the daily patterns of session lengths for each client over the last 14 days, providing insights into how productivity varies across different days and clients. By analyzing recent time-tracking data and calculating mean session lengths for each client by day of the week, it aims to understand how these patterns impact overall time allocation against target priorities.
Generated: 20260307_214719 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data
entries = query_entries(days=14)

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Group by client and day of week, calculate mean session length
df['start'] = pd.to_datetime(df['start'])
df['day_of_week'] = df['start'].dt.dayofweek
grouped_df = df.groupby(['client_name', 'day_of_week'])['duration_seconds'].mean().reset_index()

# Print results in a clear format
print(grouped_df)
