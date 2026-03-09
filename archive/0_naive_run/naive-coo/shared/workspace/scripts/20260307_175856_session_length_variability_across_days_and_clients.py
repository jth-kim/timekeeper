"""Investigation: This script investigates the primary factors contributing to session length variability across different days of the week for each client, aiming to understand how these patterns impact overall time allocation against target priorities. By analyzing recent time-tracking data and calculating mean session lengths for each client by day of the week, it provides insights into potential imbalances or patterns that could inform adjustments to priorities or alert thresholds.
Generated: 20260307_175856 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent entries
entries = query_entries(days=14)

# Convert to DataFrame
df = entries_to_dataframe(entries)

# Group by client and day of week
grouped_df = df.groupby(['client_name', 'start_dt.dt.dayofweek'])

# Calculate mean session length for each group
mean_session_lengths = grouped_df['duration_seconds'].mean()

# Print results
print(mean_session_lengths)
