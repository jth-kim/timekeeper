"""Investigation: This script investigates the relationship between task-level activities within each client and overall session length variability, aiming to understand how these activities align with the Sovereign's broader objectives. It calculates the total duration for each task within each client, sorts the results in descending order of duration, and prints the top tasks contributing to session length variability.
Generated: 20260306_225105 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

df = entries_to_dataframe(query_entries(days=30))
client_tasks = df.groupby(['client_name', 'project_name'])['duration_seconds'].sum().reset_index()
client_tasks = client_tasks.sort_values('duration_seconds', ascending=False)
print(client_tasks)
