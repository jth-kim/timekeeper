"""Investigation: This script investigates the task-level activity patterns within SEIFUKU that contribute to its variable session lengths across different days of the week. It queries the time-tracking data for the last 14 days, filters for SEIFUKU entries, and calculates the mean duration for each unique task-level activity. The results provide insights into how these activities impact overall productivity and can inform adjustments to alert thresholds.
Generated: 20260307_145427 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

df = entries_to_dataframe(query_entries(days=14))
seifuku_df = df[df['client_name'] == 'SEIFUKU']
task_level_activities = seifuku_df['description'].unique()
print(task_level_activities)

task_durations = {}
for task in task_level_activities:
    task_df = seifuku_df[seifuku_df['description'] == task]
    task_durations[task] = task_df['duration_seconds'].mean()
print(task_durations)