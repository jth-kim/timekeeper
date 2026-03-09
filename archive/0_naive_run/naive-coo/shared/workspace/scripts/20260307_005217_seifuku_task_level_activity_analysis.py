"""Investigation: This script investigates the task-level activities within SEIFUKU that contribute to its high average session duration. It queries recent time-tracking data for SEIFUKU, converts it to a DataFrame, groups by project, and calculates mean duration. The top projects contributing to SEIFUKU's high average session duration are then printed in descending order of mean duration.
Generated: 20260307_005217 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data for SEIFUKU client
seifuku_entries = [entry for entry in query_entries(days=14) if entry['client_name'] == 'SEIFUKU']

# Convert to DataFrame with proper types
df = entries_to_dataframe(seifuku_entries)

# Group by project and calculate mean duration
project_durations = df.groupby('project_name')['duration_seconds'].mean().reset_index()

# Sort projects by mean duration in descending order
project_durations = project_durations.sort_values(by='duration_seconds', ascending=False)

# Print top projects contributing to SEIFUKU's high average session duration
print(project_durations.head(5))