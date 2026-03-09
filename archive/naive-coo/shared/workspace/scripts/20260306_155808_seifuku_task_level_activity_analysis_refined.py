"""Investigation: This script investigates the task-level activities within SEIFUKU that contribute to its prolonged session durations and assesses their alignment with the Sovereign's objectives. It calculates the average session duration for SEIFUKU tasks, groups tasks by mean duration, and prints the top 5 tasks with the longest average durations.
Generated: 20260306_155808 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent SEIFUKU entries
seifuku_entries = [entry for entry in query_entries(days=14) if entry['client_name'] == 'SEIFUKU']

# Convert to DataFrame
df = entries_to_dataframe(seifuku_entries)

# Calculate average session duration for SEIFUKU tasks
average_duration = df['duration_seconds'].mean()

# Group tasks by mean duration
tasks_by_duration = df.groupby('project_name')['duration_seconds'].mean().sort_values(ascending=False)

# Print top 5 tasks with longest average durations
print(tasks_by_duration.head(5))
