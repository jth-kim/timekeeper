"""Investigation: This script investigates the underlying causes of SEIFUKU's dominance in recent sessions and assesses its impact on the Sovereign's ability to meet target allocations for other clients. It calculates average session duration, total time spent, and deviation from target allocations for each client.
Generated: 20260305_173247 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent entries
entries = query_entries(days=14)

# Convert entries to DataFrame
df = entries_to_dataframe(entries)

# Filter for SEIFUKU entries
seifuku_df = df[df['client_name'] == 'SEIFUKU']

# Calculate average session duration for SEIFUKU
avg_seifuku_duration = seifuku_df['duration_seconds'].mean()

# Calculate total time spent on SEIFUKU
total_seifuku_time = seifuku_df['duration_seconds'].sum()

# Print findings
print(f'Average session duration for SEIFUKU: {avg_seifuku_duration} seconds')
print(f'Total time spent on SEIFUKU: {total_seifuku_time} seconds')

# Investigate underlying causes of SEIFUKU's dominance
seifuku_projects = seifuku_df['project_name'].unique()
for project in seifuku_projects:
    project_df = seifuku_df[seifuku_df['project_name'] == project]
    avg_project_duration = project_df['duration_seconds'].mean()
    print(f'Average session duration for {project}: {avg_project_duration} seconds')

# Assess impact on target allocations
star_df = df[df['client_name'] == 'STAR']
bboy_df = df[df['client_name'] == 'BBOY']
boj_df = df[df['client_name'] == 'BOJ']

star_time = star_df['duration_seconds'].sum()
bboy_time = bboy_df['duration_seconds'].sum()
boj_time = boj_df['duration_seconds'].sum()

print(f'Total time spent on STAR: {star_time} seconds')
print(f'Total time spent on BBOY: {bboy_time} seconds')
print(f'Total time spent on BOJ: {boj_time} seconds')

# Calculate deviation from target allocations
target_allocations = {'STAR': 0.55, 'BBOY': 0.2, 'SEIFUKU': 0.15, 'BOJ': 0.1}
total_time = df['duration_seconds'].sum()

star_deviation = (star_time / total_time) - target_allocations['STAR']
bboy_deviation = (bboy_time / total_time) - target_allocations['BBOY']
seifuku_deviation = (total_seifuku_time / total_time) - target_allocations['SEIFUKU']
boj_deviation = (boj_time / total_time) - target_allocations['BOJ']

print(f'Deviation from target allocation for STAR: {star_deviation}')
print(f'Deviation from target allocation for BBOY: {bboy_deviation}')
print(f'Deviation from target allocation for SEIFUKU: {seifuku_deviation}')
print(f'Deviation from target allocation for BOJ: {boj_deviation}')