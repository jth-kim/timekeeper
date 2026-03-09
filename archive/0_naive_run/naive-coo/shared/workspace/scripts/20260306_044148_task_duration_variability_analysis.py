"""Investigation: This script investigates the specific factors contributing to the variability in task durations within each client and assesses their impact on overall time allocation against target priorities. It calculates the mean task duration for each client and analyzes task-level factors such as project, tags, and description to understand their influence on task duration.
Generated: 20260306_044148 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

df = entries_to_dataframe(query_entries(days=14))
# Group by client and calculate mean task duration
client_mean_durations = df.groupby('client_name')['duration_seconds'].mean()
print(client_mean_durations)

task_durations = df[['client_name', 'project_name', 'tags', 'description', 'duration_seconds']]
# Group by client, project, tags, and description to analyze task-level factors
task_factors = task_durations.groupby(['client_name', 'project_name', 'tags', 'description'])['duration_seconds'].mean()
print(task_factors)