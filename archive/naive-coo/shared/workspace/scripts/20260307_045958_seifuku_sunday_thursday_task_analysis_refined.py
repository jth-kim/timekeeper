"""Investigation: This script refines the investigation into task-level activities within SEIFUKU on Sundays and Thursdays, aiming to understand what drives longer session lengths and how these activities align with the Sovereign's broader objectives. By calculating mean session lengths for each task and printing the top tasks contributing to longer sessions, this script provides actionable insights into time allocation patterns.
Generated: 20260307_045958 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data for SEIFUKU on Sundays and Thursdays
seifuku_entries = query_entries(days=14)
seifuku_df = entries_to_dataframe(seifuku_entries)

# Filter for Sundays and Thursdays
sunday_thursday_df = seifuku_df[(seifuku_df['start'].dt.dayofweek == 6) | (seifuku_df['start'].dt.dayofweek == 3)]

# Calculate mean session lengths for each task within SEIFUKU on Sundays and Thursdays
task_level_analysis = sunday_thursday_df.groupby('description')['duration_seconds'].mean().reset_index()

# Print the top tasks contributing to longer sessions
print(task_level_analysis.sort_values(by='duration_seconds', ascending=False).head(10))
