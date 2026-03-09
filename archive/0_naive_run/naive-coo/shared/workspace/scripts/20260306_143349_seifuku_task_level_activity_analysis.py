"""Investigation: This script investigates the task-level activities within SEIFUKU that contribute to its prolonged session durations and assesses their alignment with the Sovereign's objectives. It queries recent SEIFUKU entries, converts them to a DataFrame, calculates the average session duration for SEIFUKU tasks, groups tasks by mean duration, and prints the top 5 tasks with the longest average durations.
Generated: 20260306_143349 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent SEIFUKU entries
entries = query_entries(days=14, client='SEIFUKU')

# Convert to DataFrame
df = entries_to_dataframe(entries)

# Calculate average session duration for SEIFUKU tasks
avg_duration_seifuku = df['duration_seconds'].mean()

# Group by task and calculate mean duration for each task within SEIFUKU
task_durations = df.groupby('description')['duration_seconds'].mean().reset_index()

# Sort tasks by mean duration in descending order
task_durations = task_durations.sort_values(by='duration_seconds', ascending=False)

# Print the top 5 tasks with the longest average durations
print(task_durations.head(5))
