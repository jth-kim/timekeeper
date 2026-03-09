"""Investigation: This script investigates the task-level activities within SEIFUKU that contribute to session length variability, aiming to understand how these activities align with the Sovereign's long-term goals. By analyzing recent time-tracking data and calculating mean session lengths for each task-level activity, it provides insights into potential imbalances or patterns in time allocation.
Generated: 20260307_234259 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query recent entries for SEIFUKU
entries = query_entries(days=14, client_name='SEIFUKU')

# Convert to DataFrame and calculate session lengths
df = entries_to_dataframe(entries)
df['session_length'] = df['duration_seconds']

# Group by task-level activity (description) and calculate mean session length
task_level_activities = df.groupby('description')['session_length'].mean().reset_index()

# Print results
print(task_level_activities)
