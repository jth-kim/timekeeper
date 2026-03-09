"""Investigation: This script investigates the weekly time distribution trends across clients over the last 30 days and compares these trends to the target allocations. It calculates the total time spent on each client per week, pivots the dataframe for easier comparison, and then calculates the percentage of total time spent on each client per week.
Generated: 20260305_183642 UTC
"""


from supabase_helper import query_entries, entries_to_dataframe
import pandas as pd

# Get recent entries (last 30 days)
recent_entries = query_entries(days=30)

# Convert entries to DataFrame with proper types
df = entries_to_dataframe(recent_entries)

# Calculate total time spent on each client per week
weekly_time_spent = df.groupby([pd.Grouper(key='start', freq='W'), 'client_name'])['duration_seconds'].sum().reset_index()

# Pivot the dataframe for easier comparison
pivoted_df = weekly_time_spent.pivot(index='start', columns='client_name', values='duration_seconds')

# Calculate percentage of total time spent on each client per week
total_time_per_week = pivoted_df.sum(axis=1)
percentage_per_client = (pivoted_df.div(total_time_per_week, axis=0)).fillna(0) * 100

# Print the results in a clear format
print('Weekly Time Distribution Trends Across Clients:')
print(pivoted_df)
print('\
Percentage of Total Time Spent on Each Client Per Week:')
print(percentage_per_client)