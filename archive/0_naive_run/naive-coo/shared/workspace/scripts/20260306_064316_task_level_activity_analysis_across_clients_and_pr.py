"""Investigation: This script investigates the task-level activities within each client and project that contribute to session length variability, providing insights into potential imbalances or patterns that could inform adjustments to priorities or alert thresholds.
Generated: 20260306_064316 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data
entries = query_entries(days=14)

# Convert entries to a DataFrame with proper types
df = entries_to_dataframe(entries)

# Group by client and project, calculate mean session length
grouped_df = df.groupby(['client_name', 'project_name'])['duration_seconds'].mean().reset_index()

# Print the results in a sorted format
print(grouped_df.sort_values(by='duration_seconds', ascending=False))
