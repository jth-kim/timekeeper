"""Investigation: This script investigates the underlying reasons for the observed session length variability across tasks within each client and assesses how these tasks align with the Sovereign's priorities and goals. It calculates mean session lengths for each task within clients, providing insights into potential differences in task complexity or work patterns.
Generated: 20260306_001327 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

df = entries_to_dataframe(query_entries(days=30))

task_durations = df.groupby(['client_name', 'project_name'])['duration_seconds'].mean().reset_index()

task_durations = task_durations.sort_values(by='duration_seconds', ascending=False)

print(task_durations)