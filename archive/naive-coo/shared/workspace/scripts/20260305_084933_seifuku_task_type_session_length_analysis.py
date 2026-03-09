"""Investigation: This script investigates the average session lengths for different task types within SEIFUKU over the last 14 days, providing insights into how time allocation varies across tasks and whether certain tasks require more time or attention.
Generated: 20260305_084933 UTC
"""

import pandas as pd
from supabase_helper import query_entries

df = pd.DataFrame(query_entries(days=14))
seifuku_df = df[df['client_name'] == 'SEIFUKU']
task_types = seifuku_df['tags'].unique()

for task_type in task_types:
    task_type_df = seifuku_df[seifuku_df['tags'] == task_type]
    avg_session_length = task_type_df['duration'].mean()
    print(f'Average session length for {task_type} tasks within SEIFUKU: {avg_session_length} seconds')

overall_avg_session_length = seifuku_df['duration'].mean()
print(f'Overall average session length for SEIFUKU: {overall_avg_session_length} seconds')