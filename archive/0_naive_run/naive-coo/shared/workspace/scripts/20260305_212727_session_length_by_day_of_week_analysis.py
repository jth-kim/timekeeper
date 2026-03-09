"""Investigation: This script investigates the session length patterns by day of the week for each client over the last 14 days, providing insights into how productivity varies across different days and clients. It calculates the average session length for each client and day of the week, helping to identify potential imbalances in time allocation.
Generated: 20260305_212727 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

days = 14
entries = query_entries(days=days)
df = entries_to_dataframe(entries)

df['start'] = pd.to_datetime(df['start'])
df['day_of_week'] = df['start'].dt.day_name()

grouped_df = df.groupby(['client_name', 'day_of_week'])['duration_seconds'].mean().reset_index()
print(grouped_df)