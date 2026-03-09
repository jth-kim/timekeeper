"""Investigation: This script investigates the relationship between task-level activities within SEIFUKU and their impact on overall time allocation against target priorities. It calculates the total time spent on each task within SEIFUKU, sorts tasks by duration in descending order, and prints the top tasks contributing to session length variability.
Generated: 20260307_000007 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent entries for SEIFUKU
entries = query_entries(days=14, client='SEIFUKU')

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate total time spent on each task within SEIFUKU
task_durations = df.groupby('description')['duration_seconds'].sum().reset_index()

# Sort tasks by duration in descending order
task_durations = task_durations.sort_values(by='duration_seconds', ascending=False)

# Print top tasks contributing to session length variability
print(task_durations.head(10))
