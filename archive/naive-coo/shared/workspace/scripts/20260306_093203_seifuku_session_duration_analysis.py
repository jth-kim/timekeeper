"""Investigation: This script investigates the factors contributing to the high average session duration in SEIFUKU and their impact on overall time allocation against target priorities. It calculates the average session duration for SEIFUKU, then examines the distribution of durations across projects and tasks within SEIFUKU.
Generated: 20260306_093203 UTC
"""


import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds

# Query recent entries for SEIFUKU
entries = query_entries(days=14)
seifuku_entries = [entry for entry in entries if entry['client_name'] == 'SEIFUKU']

# Convert durations to seconds and calculate average session duration
df = pd.DataFrame(seifuku_entries)
df['duration_seconds'] = df['duration'].apply(parse_duration_seconds)
average_session_duration = df['duration_seconds'].mean()

# Print findings
print(f'Average session duration for SEIFUKU: {average_session_duration} seconds')

# Investigate factors contributing to high average session duration
project_durations = df.groupby('project_name')['duration_seconds'].sum()
print(project_durations)

task_durations = df.groupby('description')['duration_seconds'].sum()
print(task_durations)
