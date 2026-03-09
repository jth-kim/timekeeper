"""Investigation: This script investigates the primary factors contributing to the variability in session lengths across different days of the week for each client and assesses their impact on overall productivity. By analyzing recent time-tracking data, calculating mean session lengths for each client by day of the week, and printing the results in a clear format, it provides insights into potential imbalances or patterns that could inform adjustments to priorities or alert thresholds.
Generated: 20260307_154105 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data
entries = query_entries(days=14)

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Group by client and day of week, calculate mean session length
df['start'] = pd.to_datetime(df['start'])
df['day_of_week'] = df['start'].dt.day_name()
grouped_df = df.groupby(['client_name', 'day_of_week'])['duration_seconds'].mean().reset_index()

# Print results
print(grouped_df)
