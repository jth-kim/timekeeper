"""Investigation: This script investigates the task-level activities within each client that contribute to session length variability and assesses their alignment with the Sovereign's objectives. It calculates the mean duration for each task within each client, providing insights into potential imbalances or patterns that could inform adjustments to priorities or alert thresholds.
Generated: 20260306_150543 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

df = entries_to_dataframe(query_entries(days=14))
print(df.head())
print(df.info())
print(df.describe())

task_durations = df.groupby('client_name')['duration_seconds'].mean()
print(task_durations)
