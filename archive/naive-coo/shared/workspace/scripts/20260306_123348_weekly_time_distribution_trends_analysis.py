"""Investigation: This script calculates the weekly time distribution trends across clients over the last 30 days and compares these trends to the target allocations. It provides insights into how time allocation varies by client and week, helping to identify potential imbalances or patterns that could inform adjustments to priorities or alert thresholds.
Generated: 20260306_123348 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent entries
entries = query_entries(days=30)

# Convert to DataFrame
df = entries_to_dataframe(entries)

# Calculate total time spent on each client per week
weekly_time_df = df.groupby('client_name')['duration_seconds'].sum().reset_index()

# Pivot the dataframe for easier comparison
pivoted_df = weekly_time_df.pivot(index='client_name', values='duration_seconds')

# Calculate percentage of total time spent on each client per week
total_time = pivoted_df.sum(axis=1)
percentage_df = (pivoted_df / total_time) * 100

# Print the results
print(percentage_df)
