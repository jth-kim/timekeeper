"""Investigation: This script investigates the task-level activities within SEIFUKU that contribute to its dominance and assesses their alignment with the Sovereign's long-term goals. By analyzing recent time-tracking data and calculating total durations for each task within SEIFUKU, it provides insights into potential areas for adjustment to ensure alignment with long-term objectives.
Generated: 20260307_222035 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

df = entries_to_dataframe(query_entries(days=14))
seifuku_df = df[df['client_name'] == 'SEIFUKU']
task_durations = seifuku_df.groupby('project_name')['duration_seconds'].sum().reset_index()
task_durations.sort_values(by='duration_seconds', ascending=False, inplace=True)
print(task_durations)