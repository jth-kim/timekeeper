"""Investigation: This script investigates the weekly time distribution trends across clients over an extended period of 90 days and compares these trends to the target allocations. It calculates the total time spent on each client per week, pivots the dataframe for easier comparison, and then calculates the percentage of total time spent on each client per week.
Generated: 20260306_160311 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data for the last 90 days
entries = query_entries(days=90)

# Convert entries to a DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate total time spent on each client per week
df['week'] = pd.to_datetime(df['start']).dt.to_period('W')
weekly_time = df.groupby(['client_name', 'week'])['duration_seconds'].sum().reset_index()

# Pivot the dataframe for easier comparison
pivoted_df = weekly_time.pivot(index='week', columns='client_name', values='duration_seconds')

# Calculate the percentage of total time spent on each client per week
total_time = pivoted_df.sum(axis=1)
percentage_df = (pivoted_df / total_time) * 100

# Print the results in a clear format
print(percentage_df)
