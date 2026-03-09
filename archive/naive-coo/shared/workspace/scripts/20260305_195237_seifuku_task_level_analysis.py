"""Investigation: This script investigates the task-level details for SEIFUKU that contribute to its high average session duration. By analyzing recent entries, calculating average session durations for each project within SEIFUKU, and comparing these averages, this investigation aims to understand how different tasks or projects within SEIFUKU impact overall time allocation against target priorities.
Generated: 20260305_195237 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent entries for SEIFUKU
entries = query_entries(days=14)
seifuku_entries = [entry for entry in entries if entry['client_name'] == 'SEIFUKU']

# Convert to DataFrame
df = entries_to_dataframe(seifuku_entries)

# Group by project and calculate average session duration
project_durations = df.groupby('project_name')['duration_seconds'].mean()

# Print results
print(project_durations)
