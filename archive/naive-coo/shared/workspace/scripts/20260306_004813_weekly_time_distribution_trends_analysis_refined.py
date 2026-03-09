"""Investigation: This script investigates the weekly time distribution trends across clients over the last 30 days and compares these trends to the target allocations. It calculates the total time spent on each client per week, pivots the dataframe for easier comparison, and then calculates the percentage of total time spent on each client per week.
Generated: 20260306_004813 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data for the last 30 days
entries = query_entries(days=30)

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate total time spent on each client per week
weekly_time_df = df.groupby(['client_name', pd.Grouper(key='start', freq='W-MON')])['duration_seconds'].sum().reset_index()

# Pivot the dataframe for easier comparison
pivoted_df = weekly_time_df.pivot(index='start', columns='client_name', values='duration_seconds')

# Calculate percentage of total time spent on each client per week
total_time_per_week = pivoted_df.sum(axis=1)
percentage_df = (pivoted_df.div(total_time_per_week, axis=0) * 100).round(2)

# Print the results in a clear format
print('Weekly Time Distribution Trends Across Clients:')
print(pivoted_df)
print('\
Percentage of Total Time Spent on Each Client per Week:')
print(percentage_df)
