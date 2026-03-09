"""Investigation: This script investigates the variability in session lengths across different projects for BBOY and calculates the average session length for each project. The goal is to understand how this variability impacts the Sovereign's ability to meet target allocations for other clients.
Generated: 20260305_184413 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent entries
entries = query_entries(days=30)

# Convert entries to DataFrame
df = entries_to_dataframe(entries)

# Filter for BBOY entries
bboy_df = df[df['client_name'] == 'BBOY']

# Calculate average session length for each project within BBOY
project_avg_session_lengths = bboy_df.groupby('project_name')['duration_seconds'].mean()

# Print the results
print(project_avg_session_lengths)
