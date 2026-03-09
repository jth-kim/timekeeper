"""Investigation: This script investigates the factors contributing to the high average session duration of SEIFUKU by analyzing recent time-tracking data, calculating average session durations for each task within SEIFUKU, and identifying the top tasks with the longest average durations.
Generated: 20260306_215026 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data for SEIFUKU
seifuku_entries = [entry for entry in query_entries(days=14) if entry['client_name'] == 'SEIFUKU']

# Convert entries to a DataFrame with proper types
df = entries_to_dataframe(seifuku_entries)

# Calculate average session duration for each task within SEIFUKU
task_durations = df.groupby('description')['duration_seconds'].mean().sort_values(ascending=False)

# Print the top 5 tasks with the longest average durations
print(task_durations.head(5))
