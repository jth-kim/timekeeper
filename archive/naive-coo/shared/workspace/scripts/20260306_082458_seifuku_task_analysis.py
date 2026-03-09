"""Investigation: This script investigates the primary tasks or activities within SEIFUKU that contribute to its high average duration and assesses their alignment with the Sovereign's long-term objectives. By analyzing recent time-tracking data, it calculates the sum of duration seconds for each task within SEIFUKU, sorts the results in descending order, and prints the top tasks.
Generated: 20260306_082458 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data for SEIFUKU
entries = query_entries(days=30)
seifuku_entries = [entry for entry in entries if entry['client_name'] == 'SEIFUKU']

# Convert to DataFrame with proper types
df = entries_to_dataframe(seifuku_entries)

# Group tasks by project name and calculate sum of duration seconds for each task
task_durations = df.groupby('project_name')['duration_seconds'].sum().reset_index()

# Sort results in descending order by duration
task_durations = task_durations.sort_values(by='duration_seconds', ascending=False)

# Print top tasks
print(task_durations.head(10))
