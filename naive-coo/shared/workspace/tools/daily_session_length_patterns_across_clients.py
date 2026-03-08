"""Investigation: This script investigates the daily patterns of session lengths for each client over the last 14 days, providing insights into how productivity varies across different days and clients.
Generated: 20260307_081224 UTC
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