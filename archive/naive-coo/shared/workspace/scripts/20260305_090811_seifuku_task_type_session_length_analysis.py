"""Investigation: This script investigates the average session lengths for different task types within SEIFUKU over the last week and compares these averages to the overall average session length for SEIFUKU, providing insights into how time allocation varies across tasks.
Generated: 20260305_090811 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query recent time-tracking data
entries = query_entries(days=7)

# Create a DataFrame from the entries
df = pd.DataFrame(entries)

# Ensure 'duration' column is in seconds for easier comparison
def duration_to_seconds(duration):
    h, m, s = map(int, duration.split(':'))
    return h * 3600 + m * 60 + s

df['duration'] = df['duration'].apply(duration_to_seconds)

# Filter for SEIFUKU entries only
seifuku_entries = df[df['client_name'] == 'SEIFUKU']

# Group by task type and calculate average session length
task_types = seifuku_entries['tags'].unique()
for task_type in task_types:
    task_entries = seifuku_entries[seifuku_entries['tags'].str.contains(task_type)]
    avg_session_length = task_entries['duration'].mean()
    print(f'Average session length for {task_type} tasks within SEIFUKU: {avg_session_length} seconds')

# Calculate overall average session length for SEIFUKU
overall_avg_session_length = seifuku_entries['duration'].mean()
print(f'Overall average session length for SEIFUKU: {overall_avg_session_length} seconds')
