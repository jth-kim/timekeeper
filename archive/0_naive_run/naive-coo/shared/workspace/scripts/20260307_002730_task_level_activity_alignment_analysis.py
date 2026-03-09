"""Investigation: This script investigates the relationship between task-level activities within each client and overall session length variability. By analyzing recent time-tracking data, it calculates mean session lengths for each task within each client and prints the top tasks contributing to session length variability. This helps understand how these tasks align with the Sovereign's broader objectives and provides insights into potential imbalances or patterns in time allocation.
Generated: 20260307_002730 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data
entries = query_entries(days=14)

# Convert to DataFrame
df = entries_to_dataframe(entries)

# Group by client and task, calculate mean session length
task_level_analysis = df.groupby(['client_name', 'project_name'])['duration_seconds'].mean().reset_index()

# Sort tasks by duration in descending order
sorted_tasks = task_level_analysis.sort_values(by='duration_seconds', ascending=False)

# Print top tasks contributing to session length variability
print(sorted_tasks.head(10))
