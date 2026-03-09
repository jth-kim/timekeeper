"""Investigation: This script analyzes task-level activities within SEIFUKU to understand what drives longer session lengths and how these tasks align with the Sovereign's broader objectives.
Generated: 20260307_034226 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

df = entries_to_dataframe(query_entries(days=14))
seifuku_df = df[df['client_name'] == 'SEIFUKU']
task_durations = seifuku_df.groupby('description')['duration_seconds'].sum().reset_index()
task_durations.sort_values(by='duration_seconds', ascending=False, inplace=True)
print(task_durations)