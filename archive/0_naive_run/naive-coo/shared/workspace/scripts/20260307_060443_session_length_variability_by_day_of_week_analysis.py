"""Investigation: This script investigates the factors contributing to the variability in session lengths across different days of the week for each client. By analyzing recent time-tracking data and calculating mean session lengths for each client by day of week, it provides insights into how productivity varies across different days and clients.
Generated: 20260307_060443 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

df = entries_to_dataframe(query_entries(days=14))
# Ensure 'start' column is datetime for grouping by day of week
df['start'] = pd.to_datetime(df['start'])
# Extract day of week from 'start'
df['day_of_week'] = df['start'].dt.day_name()
# Group by client and day of week, calculate mean session length
session_length_variability = df.groupby(['client_name', 'day_of_week'])['duration_seconds'].mean().reset_index()
print(session_length_variability)