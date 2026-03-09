"""Investigation: This script investigates the factors contributing to the variability in session lengths across different tasks within each client and assesses their impact on overall time allocation against target priorities. It calculates mean session lengths for each task within clients, providing insights into potential differences in task complexity or work patterns that could inform adjustments to priorities or alert thresholds.
Generated: 20260306_010956 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent entries
entries = query_entries(days=30)

# Convert to DataFrame
df = entries_to_dataframe(entries)

# Group by client and task, calculate mean session length
session_lengths = df.groupby(['client_name', 'project_name'])['duration_seconds'].mean().reset_index()

# Print results
print(session_lengths)
