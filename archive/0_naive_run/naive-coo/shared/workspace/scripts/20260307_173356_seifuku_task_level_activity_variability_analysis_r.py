"""Investigation: This script investigates the specific task-level activities within SEIFUKU that contribute to its variable session lengths across different days of the week. It analyzes recent time-tracking data for SEIFUKU sessions, calculates mean session lengths for each day, and identifies the top tasks contributing to session length variability.
Generated: 20260307_173356 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data for SEIFUKU sessions
entries = query_entries(days=14, client='SEIFUKU')

# Convert entries to a DataFrame with proper types
df = entries_to_dataframe(entries)

# Filter for sessions on days 3, 5, and 6 of the week
day_3_sessions = df[(df['start_dt'].dt.dayofweek == 2)]
day_5_sessions = df[(df['start_dt'].dt.dayofweek == 4)]
day_6_sessions = df[(df['start_dt'].dt.dayofweek == 5)]

# Calculate mean session lengths for each day
mean_day_3_length = day_3_sessions['duration_seconds'].mean()
mean_day_5_length = day_5_sessions['duration_seconds'].mean()
mean_day_6_length = day_6_sessions['duration_seconds'].mean()

# Print the results in a clear format
print(f'Mean session length on day 3: {mean_day_3_length} seconds')
print(f'Mean session length on day 5: {mean_day_5_length} seconds')
print(f'Mean session length on day 6: {mean_day_6_length} seconds')

# Analyze task composition of SEIFUKU sessions on these days
task_composition = df['description'].value_counts()

# Print the top tasks contributing to session length variability
print('Top tasks contributing to session length variability:')
for index, value in task_composition.head(5).items():
    print(f'{index}: {value} occurrences')
