"""Investigation: This script investigates the task-level activities within SEIFUKU on Saturdays and Thursdays that contribute to session length variability, providing insights into how these activities align with the Sovereign's broader objectives.
Generated: 20260307_080301 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query entries for SEIFUKU on Saturdays and Thursdays
entries = query_entries(days=14, client_name='SEIFUKU')

# Convert entries to dataframe
df = entries_to_dataframe(entries)

# Filter dataframe for Saturdays and Thursdays
saturday_thursday_df = df[(df['start'].dt.dayofweek == 5) | (df['start'].dt.dayofweek == 3)]

# Calculate session length variability
session_length_variability = saturday_thursday_df['duration_seconds'].std()

# Print results
print(f'Session length variability for SEIFUKU on Saturdays and Thursdays: {session_length_variability}')

# Investigate task-level activities
task_level_activities = saturday_thursday_df['description'].unique()

# Print task-level activities
print('Task-level activities within SEIFUKU on Saturdays and Thursdays:')
for activity in task_level_activities:
    print(f'- {activity}')
