"""Investigation: This script investigates the task-level activities within SEIFUKU on Sundays and Thursdays that contribute to its longer session lengths, aiming to understand how these activities align with the Sovereign's broader objectives. By calculating mean session lengths for each task and printing the top tasks contributing to longer sessions, this script provides actionable insights into time allocation patterns.
Generated: 20260307_053447 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query recent time-tracking data for SEIFUKU on Sundays and Thursdays
entries = query_entries(days=14)
seifuku_sunday_thursday_entries = [entry for entry in entries if entry['client_name'] == 'SEIFUKU' and (pd.to_datetime(entry['start']).dayofweek == 6 or pd.to_datetime(entry['start']).dayofweek == 3)]

# Convert entries to a pandas DataFrame
df = pd.DataFrame(seifuku_sunday_thursday_entries)

# Calculate mean session length for each task within SEIFUKU on Sundays and Thursdays
task_durations = df.groupby('description')['duration'].apply(lambda x: parse_duration_seconds(x.sum()))

# Print the top tasks contributing to longer sessions
print(task_durations.sort_values(ascending=False).head(10))
