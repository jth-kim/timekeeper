"""Investigation: This script investigates the factors contributing to the variability in session lengths across different days of the week for each client, providing insights into how productivity varies across different days and clients.
Generated: 20260307_024321 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

df = entries_to_dataframe(query_entries(days=14))
df['start'] = pd.to_datetime(df['start'])
df['day_of_week'] = df['start'].dt.day_name()
df_grouped = df.groupby(['client_name', 'day_of_week'])['duration_seconds'].mean().reset_index()
print(df_grouped)