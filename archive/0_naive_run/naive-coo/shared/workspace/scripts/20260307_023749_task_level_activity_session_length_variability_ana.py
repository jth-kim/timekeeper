"""Investigation: This script investigates the relationship between task-level activities within each client and overall session length variability, considering the impact of client transitions on these activities. It calculates mean session lengths for each client, analyzes task-level activities within each client, and examines the impact of client transitions on these activities.
Generated: 20260307_023749 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data
entries = query_entries(days=14)

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate session lengths in seconds
df['session_length_seconds'] = df['duration_seconds']

# Group by client and calculate mean session length
mean_session_lengths = df.groupby('client_name')['session_length_seconds'].mean()

# Investigate task-level activities within each client
task_level_activities = df.groupby(['client_name', 'project_name'])['session_length_seconds'].mean()

# Analyze the impact of client transitions on task-level activities
transition_impact = df.groupby(['previous_client', 'client_name'])['session_length_seconds'].mean()

# Print findings
print('Mean session lengths by client:')
print(mean_session_lengths)
print('\
Task-level activities within each client:')
print(task_level_activities)
print('\
Impact of client transitions on task-level activities:')
print(transition_impact)
