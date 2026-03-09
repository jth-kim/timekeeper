"""Investigation: This script investigates the primary factors contributing to session length variability across different days of the week for each client. It calculates mean session lengths for each client by day of the week, providing insights into potential imbalances or patterns that could inform adjustments to priorities or alert thresholds.
Generated: 20260307_170049 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data
entries = query_entries(days=14)

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Ensure 'start' column is datetime
df['start'] = pd.to_datetime(df['start'])

# Extract day of week from 'start'
df['day_of_week'] = df['start'].dt.dayofweek

# Group by client and day of week, calculate mean session length
grouped_df = df.groupby(['client_name', 'day_of_week'])['duration_seconds'].mean().reset_index()

# Print results
print(grouped_df)
