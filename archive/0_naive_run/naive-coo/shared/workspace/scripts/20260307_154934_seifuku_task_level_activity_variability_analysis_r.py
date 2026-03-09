"""Investigation: This script investigates the task-level activity patterns within SEIFUKU that contribute to its variable session lengths across different days of the week. It queries recent time-tracking data, filters for SEIFUKU entries, calculates mean session lengths for each day of the week, and prints the results in a clear format.
Generated: 20260307_154934 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

df = entries_to_dataframe(query_entries(days=14))
df_seifuku = df[df['client_name'] == 'SEIFUKU'].copy()

df_seifuku['day_of_week'] = pd.to_datetime(df_seifuku['start']).dt.dayofweek

df_seifuku_grouped = df_seifuku.groupby('day_of_week')['duration_seconds'].mean().reset_index()

df_seifuku_grouped['day_of_week'] = df_seifuku_grouped['day_of_week'].apply(lambda x: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][x])

print(df_seifuku_grouped)
