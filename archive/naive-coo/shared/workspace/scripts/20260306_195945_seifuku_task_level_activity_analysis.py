"""Investigation: This script investigates specific task-level activities within SEIFUKU that contribute to its high average session duration and proposes concrete actions to address potential imbalances in time allocation.
Generated: 20260306_195945 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query recent entries for SEIFUKU
entries = query_entries(days=14, client='SEIFUKU')

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Group by task (description) and calculate mean session duration
task_durations = df.groupby('description')['duration_seconds'].mean().reset_index()

# Sort tasks by mean duration in descending order
task_durations = task_durations.sort_values(by='duration_seconds', ascending=False)

# Print the top 5 tasks with the longest mean durations
print(task_durations.head(5))
