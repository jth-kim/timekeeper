"""Investigation: This script investigates the underlying reasons for the observed session length variability across tasks within each client by analyzing recent time-tracking data and calculating mean session lengths for each task. It aims to understand how these tasks align with the Sovereign's priorities and goals, providing insights into potential imbalances or patterns that could inform adjustments to priorities or alert thresholds.
Generated: 20260306_005800 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data
entries = query_entries(days=14)

# Convert to DataFrame
df = entries_to_dataframe(entries)

# Calculate session lengths in seconds
df['session_length_seconds'] = df['duration_seconds']

# Group by client and task, calculate mean session length
task_level_data = df.groupby(['client_name', 'project_name'])['session_length_seconds'].mean().reset_index()

# Print the results
print(task_level_data)
