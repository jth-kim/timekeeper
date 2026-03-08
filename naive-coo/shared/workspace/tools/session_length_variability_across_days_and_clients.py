"""Investigation: This script investigates the primary factors contributing to session length variability across different days of the week for each client. It calculates mean session lengths for each client by day of the week, providing insights into potential imbalances or patterns that could inform adjustments to priorities or alert thresholds.
Generated: 20260307_191731 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

df = entries_to_dataframe(query_entries(days=14))
# Convert 'start' column to datetime format for easier grouping by day of week
df['start'] = pd.to_datetime(df['start'])
# Extract day of the week from 'start' column
df['day_of_week'] = df['start'].dt.day_name()
# Group data by client and day of the week, then calculate mean session length for each group
grouped_df = df.groupby(['client_name', 'day_of_week'])['duration_seconds'].mean().reset_index()
print(grouped_df)