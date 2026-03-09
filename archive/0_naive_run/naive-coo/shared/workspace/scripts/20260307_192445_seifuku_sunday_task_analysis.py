"""Investigation: This script investigates the most time-consuming tasks within SEIFUKU on Sundays by analyzing recent time-tracking data, calculating total duration for each task, and printing the top 3 tasks with the longest durations.
Generated: 20260307_192445 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data for SEIFUKU sessions on Sundays
sunday_seifuku_entries = [entry for entry in query_entries(days=14) if 'SEIFUKU' in entry['client_name'] and entry['start'].weekday() == 6]

# Convert to DataFrame with proper types
df_sunday_seifuku = entries_to_dataframe(sunday_seifuku_entries)

# Calculate total duration for each task within SEIFUKU on Sundays
task_durations = df_sunday_seifuku.groupby('description')['duration_seconds'].sum().sort_values(ascending=False)

# Print the top 3 most time-consuming tasks
print(task_durations.head(3))
