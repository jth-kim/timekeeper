"""Investigation: This script aims to investigate the underlying reasons for the observed session length variability across tasks within each client by analyzing recent time-tracking data and calculating mean session lengths for each task. It will provide insights into potential differences in task complexity, client requirements, or work patterns that could impact overall time allocation against target priorities.
Generated: 20260305_234443 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data for the last two weeks
entries = query_entries(days=14)

# Convert entries to a DataFrame with proper types
df = entries_to_dataframe(entries)

# Group by client and task, calculate mean session length
task_level_analysis = df.groupby(['client_name', 'project_name'])['duration_seconds'].mean().reset_index()

# Print the result in a clear format
print(task_level_analysis.to_string(index=False))
