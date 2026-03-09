"""Investigation: This script investigates task-level activities within each client that contribute to session length variability and assesses their alignment with the Sovereign's objectives. It calculates mean session durations for each task within each client, providing insights into potential imbalances or patterns that could inform adjustments to priorities or alert thresholds.
Generated: 20260306_175308 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data
entries = query_entries(days=14)

# Convert to DataFrame for easier analysis
df = entries_to_dataframe(entries)

# Group by client and project, calculate mean session duration
mean_durations = df.groupby(['client_name', 'project_name'])['duration_seconds'].mean().reset_index()

# Print the results in a readable format
print(mean_durations.to_string(index=False))
