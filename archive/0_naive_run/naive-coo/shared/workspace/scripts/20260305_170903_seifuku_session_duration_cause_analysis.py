"""Investigation: This script investigates the underlying causes of SEIFUKU's longer average session durations compared to other clients and assesses their impact on overall time allocation against target priorities.
Generated: 20260305_170903 UTC
"""


import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds

# Query recent entries
entries = query_entries(days=14)

# Convert entries to DataFrame
df = pd.DataFrame(entries)

# Calculate duration in seconds
df['duration_seconds'] = df['duration'].apply(parse_duration_seconds)

# Group by client and calculate average session duration
avg_session_durations = df.groupby('client_name')['duration_seconds'].mean()

# Print average session durations for each client
print(avg_session_durations)

# Filter for SEIFUKU entries
seifuku_entries = df[df['client_name'] == 'SEIFUKU']

# Calculate average session duration for SEIFUKU
avg_seifuku_duration = seifuku_entries['duration_seconds'].mean()

# Print average session duration for SEIFUKU
print(f'Average session duration for SEIFUKU: {avg_seifuku_duration} seconds')

# Investigate project distribution within SEIFUKU
seifuku_projects = seifuku_entries['project_name'].unique()
print(f'SEIFUKU projects: {seifuku_projects}')

# Calculate average time spent on each project within SEIFUKU
avg_project_durations = seifuku_entries.groupby('project_name')['duration_seconds'].mean()
print(avg_project_durations)
