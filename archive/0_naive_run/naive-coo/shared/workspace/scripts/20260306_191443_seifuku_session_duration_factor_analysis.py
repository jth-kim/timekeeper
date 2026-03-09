"""Investigation: This script investigates the factors contributing to the high average session duration in SEIFUKU by analyzing recent time-tracking data, calculating statistics such as mean and standard deviation of session durations, and examining task-level activities within SEIFUKU. The goal is to understand how these factors impact overall productivity and goal achievement.
Generated: 20260306_191443 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data for SEIFUKU
entries = query_entries(days=14, client='SEIFUKU')

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate average session duration and other statistics for SEIFUKU sessions
avg_session_duration = df['duration_seconds'].mean()
std_dev = df['duration_seconds'].std()

print(f'Average session duration for SEIFUKU: {avg_session_duration} seconds')
print(f'Standard deviation of session durations for SEIFUKU: {std_dev} seconds')

# Investigate factors contributing to high average session duration
# For example, calculate mean duration for each task within SEIFUKU and print results
task_durations = df.groupby('project_name')['duration_seconds'].mean()
print(task_durations)
