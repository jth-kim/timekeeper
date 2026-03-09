"""Investigation: This script analyzes the time allocation for each project within SEIFUKU, providing insights into how these projects contribute to the client's overall dominance in time allocation.
Generated: 20260307_065158 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query entries for SEIFUKU client
entries = query_entries(days=14)
seifuku_entries = [entry for entry in entries if entry['client_name'] == 'SEIFUKU']

# Convert entries to DataFrame with proper types
df = entries_to_dataframe(seifuku_entries)

# Group by project and calculate total time spent on each project
project_time_allocations = df.groupby('project_name')['duration_seconds'].sum().reset_index()

# Print the results
print(project_time_allocations)
