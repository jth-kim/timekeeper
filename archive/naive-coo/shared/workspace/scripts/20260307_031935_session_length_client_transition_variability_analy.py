"""Investigation: This script investigates the relationship between session length variability and client transitions across different days of the week, aiming to understand how these factors impact overall time allocation against target priorities.
Generated: 20260307_031935 UTC
"""

import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds, entries_to_dataframe

df = entries_to_dataframe(query_entries(days=14))
df['start'] = pd.to_datetime(df['start'])
df['day_of_week'] = df['start'].dt.dayofweek

df_grouped = df.groupby(['client_name', 'day_of_week'])['duration_seconds'].mean().reset_index()
print(df_grouped)