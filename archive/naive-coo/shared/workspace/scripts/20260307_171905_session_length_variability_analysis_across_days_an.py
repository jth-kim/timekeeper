"""Investigation: This script investigates the primary factors contributing to session length variability across different days of the week for each client. It calculates mean session lengths for each client by day of the week, providing insights into potential imbalances or patterns that could inform adjustments to priorities or alert thresholds.
Generated: 20260307_171905 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data
entries = query_entries(days=14)

# Convert entries to a DataFrame with proper types
df = entries_to_dataframe(entries)

# Group by client and day of the week, calculate mean session length
grouped_df = df.groupby(['client_name', 'start_dt.dt.dayofweek'])['duration_seconds'].mean().reset_index()

# Print the results in a clear format
print(grouped_df.to_string(index=False))
