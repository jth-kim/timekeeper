"""Investigation: This script investigates the task-level activities within SEIFUKU's Self Authoring project that contribute to its high duration and assesses their alignment with the Sovereign's long-term objectives. It calculates the total duration for each task, sorts tasks by duration in descending order, and prints the top 5 tasks. Additionally, it calculates the average session length for each task, sorts tasks by average session length in descending order, and prints the top 5 tasks.
Generated: 20260306_091507 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data for SEIFUKU's Self Authoring project
entries = query_entries(days=60)
seifuku_self_authoring_entries = [entry for entry in entries if 'SEIFUKU' in entry['client_name'] and 'Self Authoring' in entry['project_name']]

# Convert entries to a DataFrame with proper types
df = entries_to_dataframe(seifuku_self_authoring_entries)

# Calculate the total duration for each task within SEIFUKU's Self Authoring project
task_durations = df.groupby('description')['duration_seconds'].sum().reset_index()

# Sort tasks by duration in descending order and print the top 5 tasks
top_tasks = task_durations.sort_values(by='duration_seconds', ascending=False).head(5)
print(top_tasks)

# Calculate the average session length for each task within SEIFUKU's Self Authoring project
task_session_lengths = df.groupby('description')['duration_seconds'].mean().reset_index()

# Sort tasks by average session length in descending order and print the top 5 tasks
top_tasks_by_session_length = task_session_lengths.sort_values(by='duration_seconds', ascending=False).head(5)
print(top_tasks_by_session_length)
