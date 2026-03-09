"""Investigation: This script investigates the specific task-level activities within SEIFUKU that contribute to its dominance, aiming to understand how these activities align with the Sovereign's long-term goals. By analyzing recent time-tracking data and calculating mean durations for each task-level activity, it provides insights into potential imbalances or patterns that could inform adjustments to priorities or alert thresholds.
Generated: 20260307_211341 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data for SEIFUKU
entries = query_entries(days=14, client='SEIFUKU')

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Group by task-level activity (description) and calculate mean duration
task_durations = df.groupby('description')['duration_seconds'].mean().reset_index()

# Sort by mean duration in descending order
task_durations = task_durations.sort_values(by='duration_seconds', ascending=False)

# Print top 5 tasks with longest mean durations
print(task_durations.head(5))
