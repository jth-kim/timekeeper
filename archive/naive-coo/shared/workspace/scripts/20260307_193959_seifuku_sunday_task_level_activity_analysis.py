"""Investigation: This script investigates the task-level activity patterns within SEIFUKU on Sundays that contribute to its variable session lengths. It queries recent time-tracking data, converts it to a pandas DataFrame, calculates session lengths in seconds, groups by task-level activity (description), and prints the top 3 tasks with the longest mean session lengths.
Generated: 20260307_193959 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data for SEIFUKU on Sundays
sunday_seifuku_entries = [entry for entry in query_entries(days=14) if 'SEIFUKU' in entry['client_name'] and entry['start'].weekday() == 6]

# Convert entries to DataFrame with proper types
df = entries_to_dataframe(sunday_seifuku_entries)

# Calculate session lengths in seconds
df['session_length_seconds'] = df['duration_seconds']

# Group by task-level activity (description) and calculate mean session length
task_level_activity_means = df.groupby('description')['session_length_seconds'].mean()

# Print the top 3 tasks with the longest mean session lengths
print(task_level_activity_means.nlargest(3))
