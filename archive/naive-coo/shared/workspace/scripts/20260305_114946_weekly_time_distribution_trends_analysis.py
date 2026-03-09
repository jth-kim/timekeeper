"""Investigation: This script analyzes the weekly time distribution trends across clients over the last 30 days and compares these trends to the target allocations. It calculates the total time spent on each client per week, pivots the dataframe for easier comparison, and then calculates the percentage of total time spent on each client per week.
Generated: 20260305_114946 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent entries (last 30 days)
recent_entries = query_entries(days=30)

# Convert to DataFrame with proper types
df = entries_to_dataframe(recent_entries)

# Calculate total time spent on each client per week
weekly_time_df = df.groupby('client_name')['duration_seconds'].sum().reset_index()

# Pivot for easier comparison
pivoted_df = weekly_time_df.pivot(index='client_name', columns='week', values='duration_seconds')

# Calculate percentage of total time spent on each client per week
total_time_per_week = pivoted_df.sum(axis=0)
percentage_df = (pivoted_df / total_time_per_week) * 100

# Print results
print(percentage_df)
