"""Investigation: This script analyzes task-level activities within each client to understand how these tasks contribute to session length variability and align with the Sovereign's priorities and goals.
Generated: 20260305_233905 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

df = entries_to_dataframe(query_entries(days=14))
# Filter for each client and calculate mean session length for tasks within that client
task_lengths = df.groupby(['client_name', 'project_name'])['duration_seconds'].mean().reset_index()
task_lengths.columns = ['Client', 'Task', 'Mean Session Length']
print(task_lengths)
