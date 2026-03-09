"""Investigation: This script investigates the task-level activity patterns within SEIFUKU on Sundays, focusing on both task types and durations to understand their contribution to variable session lengths. By analyzing recent time-tracking data, calculating mean session lengths for each task-level activity, and printing the results in a clear format, it provides insights into potential imbalances or patterns that could inform adjustments to priorities or alert thresholds.
Generated: 20260307_194538 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe
# Query recent time-tracking data for SEIFUKU on Sundays
df = entries_to_dataframe(query_entries(days=14))
# Filter for SEIFUKU and Sunday sessions
df_seifuku_sunday = df[(df['client_name'] == 'SEIFUKU') & (df['start'].dt.dayofweek == 6)]
# Calculate session lengths in seconds
session_lengths = df_seifuku_sunday['duration_seconds']
# Group by task-level activity (description) and calculate mean session length
mean_session_lengths = session_lengths.groupby(df_seifuku_sunday['description']).mean()
print(mean_session_lengths)