"""Investigation: This script investigates the task-level activities within SEIFUKU that contribute to its prolonged session durations and assesses their alignment with the Sovereign's objectives. It queries recent SEIFUKU entries, converts them to a DataFrame, calculates average session duration for SEIFUKU tasks, groups tasks by mean duration, and prints the top 5 tasks with the longest average durations.
Generated: 20260306_153135 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent SEIFUKU entries
seifuku_entries = query_entries(days=14, client='SEIFUKU')

# Convert to DataFrame and calculate average session duration for SEIFUKU tasks
df = entries_to_dataframe(seifuku_entries)
df['session_duration'] = df['duration_seconds'] / 3600  # Convert seconds to hours
seifuku_avg_session_duration = df['session_duration'].mean()
print(f'SEIFUKU average session duration: {seifuku_avg_session_duration} hours')

# Group tasks by mean duration and print top 5 tasks with longest average durations
task_durations = df.groupby('description')['session_duration'].mean().reset_index()
task_durations = task_durations.sort_values(by='session_duration', ascending=False).head(5)
print(task_durations)