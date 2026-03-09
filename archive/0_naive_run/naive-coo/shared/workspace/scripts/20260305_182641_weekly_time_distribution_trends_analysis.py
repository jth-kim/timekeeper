"""Investigation: This script investigates the weekly time distribution trends across clients over the last 30 days and compares these trends to the target allocations. It calculates the total time spent on each client per week, pivots the dataframe for easier comparison, and then calculates the percentage of total time spent on each client per week.
Generated: 20260305_182641 UTC
"""


import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds

# Query entries for the last 30 days
entries = query_entries(days=30)

# Convert entries to a DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate total time spent on each client per week
weekly_time_df = df.groupby(['client_name', pd.Grouper(key='start', freq='W')])['duration_seconds'].sum().reset_index()

# Pivot the dataframe for easier comparison
pivoted_df = weekly_time_df.pivot(index='start', columns='client_name', values='duration_seconds')

# Calculate percentage of total time spent on each client per week
total_time_df = pivoted_df.div(pivoted_df.sum(axis=1), axis=0)

# Print the results
print(total_time_df)
