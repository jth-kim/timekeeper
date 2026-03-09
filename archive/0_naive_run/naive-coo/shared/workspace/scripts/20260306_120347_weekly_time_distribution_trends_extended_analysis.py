"""Investigation: This script investigates the weekly time distribution trends across clients over an extended period of 120 days and compares these trends to the target allocations. It calculates the total time spent on each client per week, pivots the dataframe for easier comparison, and then calculates the percentage of total time spent on each client per week.
Generated: 20260306_120347 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data for the last 120 days
entries = query_entries(days=120)

# Convert entries to a pandas DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate total time spent on each client per week
weekly_time_df = df.groupby('client_name')['duration_seconds'].sum().reset_index()
weekly_time_df['week'] = pd.to_datetime(weekly_time_df.index).dt.to_period('W')

# Pivot the dataframe for easier comparison
pivoted_df = weekly_time_df.pivot(index='week', columns='client_name', values='duration_seconds')

# Calculate the percentage of total time spent on each client per week
percentage_df = pivoted_df.div(pivoted_df.sum(axis=1), axis=0) * 100

# Print the results
print(percentage_df)
