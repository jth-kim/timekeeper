"""Investigation: This script investigates the task-level activities within SEIFUKU that contribute to its high average session duration and assesses their impact on overall productivity and goal achievement. It calculates the mean session duration for each task within SEIFUKU and prints the results in a sorted format, allowing for easy identification of tasks with the longest durations.
Generated: 20260306_201627 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data for SEIFUKU
entries = query_entries(days=14, client='SEIFUKU')

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate mean session duration for each task within SEIFUKU
mean_durations = df.groupby('project_name')['duration_seconds'].mean()

# Print the results in a sorted format
print(mean_durations.sort_values(ascending=False))
