"""Investigation: This script investigates the task-level activities within SEIFUKU that contribute to its prolonged session durations and assesses their alignment with the Sovereign's objectives. It queries recent entries for SEIFUKU, converts them to a DataFrame, calculates session lengths and task durations, and prints these findings.
Generated: 20260306_134023 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent entries for SEIFUKU
entries = query_entries(days=14, client='SEIFUKU')

# Convert to DataFrame
df = entries_to_dataframe(entries)

# Calculate session lengths and task durations
session_lengths = df['duration_seconds']
task_durations = df.groupby('project_name')['duration_seconds'].sum()

# Print findings
print('Session lengths for SEIFUKU:', session_lengths)
print('Task durations for SEIFUKU:', task_durations)
