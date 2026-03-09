"""Investigation: This script investigates the patterns of session lengths and task-level activities within each client across different days of the week, providing insights into how productivity varies across different days and clients. By analyzing recent time-tracking data, calculating mean session lengths for each client by day of the week, and printing the results in a clear format, it aims to understand how these patterns impact overall time allocation against target priorities.
Generated: 20260307_212853 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

df = entries_to_dataframe(query_entries(days=14))
print(df.head())

task_durations = df.groupby('client_name')['duration_seconds'].mean()
print(task_durations)
