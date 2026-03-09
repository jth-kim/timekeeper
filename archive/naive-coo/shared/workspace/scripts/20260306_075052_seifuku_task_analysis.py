"""Investigation: This script investigates the primary tasks or activities within SEIFUKU that contribute to its high hour total and assesses their alignment with the Sovereign's long-term goals. It queries recent time-tracking data, filters for SEIFUKU entries, groups tasks by project name, calculates the sum of duration seconds for each task, sorts the results in descending order, and prints the top tasks.
Generated: 20260306_075052 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

current_entries = query_entries(days=14)
df = entries_to_dataframe(current_entries)
seifuku_df = df[df['client_name'] == 'SEIFUKU']
task_durations = seifuku_df.groupby('project_name')['duration_seconds'].sum().reset_index()
task_durations.sort_values(by='duration_seconds', ascending=False, inplace=True)
print(task_durations)