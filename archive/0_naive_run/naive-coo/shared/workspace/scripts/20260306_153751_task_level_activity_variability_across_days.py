"""Investigation: This script investigates task-level activities within each client that contribute to session length variability across different days of the week. By analyzing recent time-tracking data and calculating mean session durations for each client and day of week, it provides insights into how these activities align with the Sovereign's objectives and potential areas for optimization.
Generated: 20260306_153751 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data for all clients
entries = query_entries(days=14)
df = entries_to_dataframe(entries)

# Group by client and day of week to analyze session length variability
df['day_of_week'] = df['start'].dt.dayofweek
grouped_df = df.groupby(['client_name', 'day_of_week'])['duration_seconds'].mean().reset_index()

# Print the results in a clear format
print(grouped_df.to_string(index=False))