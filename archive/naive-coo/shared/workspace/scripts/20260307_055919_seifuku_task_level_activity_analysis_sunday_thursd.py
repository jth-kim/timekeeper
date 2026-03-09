"""Investigation: This script investigates the task-level activities within SEIFUKU that contribute to its longer session lengths on Sundays and Thursdays, aiming to understand how these activities align with the Sovereign's broader objectives. By analyzing recent time-tracking data and calculating mean session lengths for each task, it provides insights into potential imbalances or patterns in time allocation.
Generated: 20260307_055919 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

df = entries_to_dataframe(query_entries(days=14))
seifuku_df = df[df['client_name'] == 'SEIFUKU']
sunday_seifuku_df = seifuku_df[seifuku_df['start'].dt.dayofweek == 6]
thursday_seifuku_df = seifuku_df[seifuku_df['start'].dt.dayofweek == 3]

sunday_task_durations = sunday_seifuku_df.groupby('description')['duration_seconds'].sum()
thursday_task_durations = thursday_seifuku_df.groupby('description')['duration_seconds'].sum()

top_sunday_tasks = sunday_task_durations.nlargest(5)
top_thursday_tasks = thursday_task_durations.nlargest(5)

print("Top tasks on Sundays:")
print(top_sunday_tasks)
print("\nTop tasks on Thursdays:")
print(top_thursday_tasks)