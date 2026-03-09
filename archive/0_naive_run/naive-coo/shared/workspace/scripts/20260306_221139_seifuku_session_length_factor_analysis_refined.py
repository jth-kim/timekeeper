"""Investigation: This script investigates the factors contributing to SEIFUKU's high average session duration by analyzing recent time-tracking data, calculating average session durations for each task within SEIFUKU, and identifying the top tasks with the longest average durations.
Generated: 20260306_221139 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data for SEIFUKU
entries = query_entries(days=30)
seifuku_entries = [entry for entry in entries if entry['client_name'] == 'SEIFUKU']

# Convert to DataFrame with proper types
df_seifuku = entries_to_dataframe(seifuku_entries)

# Calculate average session duration for each task within SEIFUKU
task_durations = df_seifuku.groupby('description')['duration_seconds'].mean().reset_index()

# Sort tasks by average duration in descending order
task_durations = task_durations.sort_values(by='duration_seconds', ascending=False)

# Print top 5 tasks with longest average durations
print(task_durations.head(5))
