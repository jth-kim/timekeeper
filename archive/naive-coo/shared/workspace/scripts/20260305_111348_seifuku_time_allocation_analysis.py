"""Investigation: This script investigates the specific factors contributing to the high percentage of time allocated to SEIFUKU over the last 30 days and assesses whether these factors align with the Sovereign's long-term goals. It calculates the total time spent on SEIFUKU, average session length for SEIFUKU, and examines tasks within SEIFUKU that contribute to its longer average session lengths.
Generated: 20260305_111348 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

df = entries_to_dataframe(query_entries(days=30))
seifuku_df = df[df['client_name'] == 'SEIFUKU']
total_seifuku_time = seifuku_df['duration_seconds'].sum()
print(f'Total time spent on SEIFUKU: {total_seifuku_time} seconds')

# Calculate average session length for SEIFUKU
average_session_length = seifuku_df['duration_seconds'].mean()
print(f'Average session length for SEIFUKU: {average_session_length} seconds')

# Investigate tasks within SEIFUKU that contribute to its longer average session lengths
seifuku_tasks = seifuku_df['project_name'].unique()
for task in seifuku_tasks:
    task_df = seifuku_df[seifuku_df['project_name'] == task]
    print(f'Task: {task}, Average session length: {task_df[