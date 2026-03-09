"""Investigation: This script investigates the relationship between session lengths and client transitions over the last 14 days. It calculates mean session lengths for each client and project, as well as total time spent on each client. The results provide insights into how time allocation varies across different clients and projects, and can inform adjustments to priorities or alert thresholds.
Generated: 20260305_174327 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent entries (last 14 days)
entries = query_entries(days=14)

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Group by client and project, calculate mean session length
client_project_means = df.groupby(['client_name', 'project_name'])['duration_seconds'].mean().reset_index()

# Calculate total time spent on each client
total_time_per_client = df.groupby('client_name')['duration_seconds'].sum().reset_index()

# Merge the two dataframes for easier comparison
merged_df = pd.merge(client_project_means, total_time_per_client, on='client_name', suffixes=('_mean', '_total'))

# Print the results in a clear format
print(merged_df.to_string(index=False))
