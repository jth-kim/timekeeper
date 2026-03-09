"""Investigation: This script investigates the weekly time distribution trends across clients over an extended period of 60 days and compares these trends to the target allocations. It calculates the total time spent on each client per week, pivots the DataFrame for easier comparison, and then calculates the percentage of total time spent on each client per week.
Generated: 20260306_134946 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query entries for the last 60 days
entries = query_entries(days=60)

# Convert entries to a DataFrame
df = entries_to_dataframe(entries)

# Calculate total time spent on each client per week
weekly_time_df = df.groupby([pd.Grouper(key='start', freq='W'), 'client_name'])['duration_seconds'].sum().reset_index()

# Pivot the DataFrame for easier comparison
pivoted_df = weekly_time_df.pivot(index='start', columns='client_name', values='duration_seconds')

# Calculate the percentage of total time spent on each client per week
percentage_df = pivoted_df.div(pivoted_df.sum(axis=1), axis=0) * 100

# Print the results
print(percentage_df)
