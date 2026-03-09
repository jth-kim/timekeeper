"""Investigation: This script investigates the primary factors contributing to session length variability across different days of the week for each client, aiming to understand how productivity varies and whether there are patterns that could inform adjustments to priorities or alert thresholds.
Generated: 20260307_175018 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data
entries = query_entries(days=14)

# Convert to dataframe with proper types
df = entries_to_dataframe(entries)

# Ensure 'start' column is datetime for grouping
df['start'] = pd.to_datetime(df['start'])

# Group by client and day of week, calculate mean session length
grouped_df = df.groupby([pd.Grouper(key='start', freq='D'), 'client_name'])['duration_seconds'].mean().reset_index()

# Print results to understand patterns
print(grouped_df)
