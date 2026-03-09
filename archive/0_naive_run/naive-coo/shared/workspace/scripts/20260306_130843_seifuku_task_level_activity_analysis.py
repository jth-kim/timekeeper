"""Investigation: This script investigates the task-level activities within SEIFUKU that contribute to its prolonged session durations, aiming to understand how these tasks align with the Sovereign's objectives and potentially identify areas for optimization in time allocation.
Generated: 20260306_130843 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query recent entries for SEIFUKU
seifuku_entries = [entry for entry in query_entries(days=14) if entry['client_name'] == 'SEIFUKU']

# Convert to DataFrame
df = pd.DataFrame(seifuku_entries)

# Calculate session lengths in seconds
df['duration_seconds'] = df['duration'].apply(lambda x: parse_duration_seconds(x))

# Group by task (description) and calculate mean duration
task_durations = df.groupby('description')['duration_seconds'].mean().reset_index()

# Sort tasks by mean duration in descending order
task_durations = task_durations.sort_values(by='duration_seconds', ascending=False)

# Print the top 5 tasks with the longest mean durations
print(task_durations.head(5))
