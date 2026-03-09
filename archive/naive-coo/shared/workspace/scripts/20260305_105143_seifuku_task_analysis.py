"""Investigation: This script investigates the specific tasks within SEIFUKU that contribute to its longer average session lengths and assesses whether these tasks align with the Sovereign's long-term goals.
Generated: 20260305_105143 UTC
"""


import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds

# Query recent entries for SEIFUKU
entries = query_entries(days=30)
seifuku_entries = [e for e in entries if e['client_name'] == 'SEIFUKU']

# Convert to DataFrame and calculate session lengths
df = pd.DataFrame(seifuku_entries)
df['duration_seconds'] = df['duration'].apply(parse_duration_seconds)

# Group by project and task, calculate average session length
project_avg_lengths = df.groupby('project_name')['duration_seconds'].mean()
task_avg_lengths = df.groupby('description')['duration_seconds'].mean()

# Print findings
print('Average session lengths for SEIFUKU projects:')
print(project_avg_lengths)
print('Average session lengths for SEIFUKU tasks:')
print(task_avg_lengths)

# Compare with target allocations to assess alignment
target_allocations = {'STAR': 0.55, 'SEIFUKU': 0.15, 'BBOY': 0.2, 'BOJ': 0.1}
seifuku_target = target_allocations['SEIFUKU']
print(f'SEIFUKU target allocation: {seifuku_target}')

# Assess alignment based on average session lengths and target
if project_avg_lengths.max() > (seifuku_target * 3600):
    print('Warning: SEIFUKU tasks may be dominating time allocation, potentially misaligning with long-term goals.')
else:
    print('SEIFUKU task durations appear aligned with target allocations.')