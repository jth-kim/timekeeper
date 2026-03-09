"""Investigation: This script investigates the task-level activities within each client that contribute to session length variability and assesses their impact on overall time allocation against target priorities. It calculates the mean session length for each client and project, providing insights into potential imbalances or patterns that could inform adjustments to alert thresholds configuration.
Generated: 20260306_054655 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data
entries = query_entries(days=14)

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Group by client and project
grouped_df = df.groupby(['client_name', 'project_name'])

# Calculate mean session length for each group
mean_session_lengths = grouped_df['duration_seconds'].mean()

# Print results in a clear format
print(mean_session_lengths)
