"""Investigation: This script investigates the task-level activities within SEIFUKU that contribute to its longer session lengths and assesses their alignment with the Sovereign's broader objectives. It queries recent time-tracking data for SEIFUKU, calculates mean session lengths for each task, and prints the top tasks contributing to longer sessions.
Generated: 20260307_041847 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data for SEIFUKU
seifuku_entries = [entry for entry in query_entries(days=14) if entry['client_name'] == 'SEIFUKU']

# Convert to DataFrame with proper types
df = entries_to_dataframe(seifuku_entries)

# Calculate mean session length for each task within SEIFUKU
task_durations = df.groupby('description')['duration_seconds'].mean().reset_index()

# Sort tasks by duration in descending order
task_durations = task_durations.sort_values(by='duration_seconds', ascending=False)

# Print top 5 tasks contributing to longer session lengths
print(task_durations.head(5))
