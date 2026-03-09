"""Investigation: This script investigates task-level activity patterns within SEIFUKU on Saturdays and assesses their impact on overall time allocation against target priorities. By analyzing recent time-tracking data, calculating mean session lengths for each project, and plotting task durations, it provides insights into potential imbalances or patterns that could inform adjustments to alert thresholds configuration.
Generated: 20260307_120433 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

df = entries_to_dataframe(query_entries(days=14))
seifuku_df = df[df['client_name'] == 'SEIFUKU']
saturday_df = seifuku_df[seifuku_df['start'].dt.dayofweek == 5]
task_durations = saturday_df.groupby('project_name')['duration_seconds'].sum()
print(task_durations)