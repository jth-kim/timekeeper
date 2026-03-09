"""Investigation: This script investigates the task-level activities within STAR that contribute to its prolonged session durations and assesses their alignment with the Sovereign's objectives. It queries recent entries for STAR, converts them to a DataFrame, calculates session lengths and task durations, and prints these findings.
Generated: 20260306_141328 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent entries for STAR
entries = query_entries(days=14, client='STAR')

# Convert to DataFrame
df = entries_to_dataframe(entries)

# Calculate session lengths and task durations
session_lengths = df['duration_seconds']
task_durations = df.groupby('project_name')['duration_seconds'].sum()

# Print findings
print('Session lengths for STAR:')
print(session_lengths)
print('\
Task durations for STAR:')
print(task_durations)
