"""Investigation: This script investigates the weekly time distribution trends across clients over the last 30 days, comparing these trends to the target allocations. It calculates total hours spent on each client per week, pivots the dataframe for easier comparison, and then calculates the percentage of total time spent on each client per week.
Generated: 20260306_075644 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data for the last 30 days
entries = query_entries(days=30)

# Convert entries to a DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate total hours spent on each client per week
df['week'] = pd.Grouper(key='start', freq='W')
weekly_hours = df.groupby('client_name')['duration_seconds'].sum() / 3600

# Pivot the dataframe for easier comparison
pivoted_df = weekly_hours.unstack()

# Calculate percentage of total time spent on each client per week
total_hours_per_week = pivoted_df.sum(axis=1)
percentage_per_client = (pivoted_df.div(total_hours_per_week, axis=0) * 100)

# Print findings in a clear format
print('Weekly Time Distribution Trends Across Clients:')
print(pivoted_df)
print('\
Percentage of Total Time Spent on Each Client Per Week:')
print(percentage_per_client)
