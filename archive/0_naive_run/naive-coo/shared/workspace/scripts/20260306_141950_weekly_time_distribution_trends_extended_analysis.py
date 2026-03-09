"""Investigation: This script investigates the weekly time distribution trends across clients over an extended period of 90 days and compares these trends to the target allocations. It calculates the total time spent on each client per week, pivots the DataFrame for easier comparison, and then calculates the percentage of total time spent on each client per week.
Generated: 20260306_141950 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query entries for the last 90 days
entries = query_entries(days=90)

# Convert entries to a DataFrame
df = entries_to_dataframe(entries)

# Calculate total time spent on each client per week
df['week'] = df['start'].dt.to_period('W')
df['client_time'] = df.groupby(['week', 'client_name'])['duration_seconds'].sum().reset_index()

# Pivot the DataFrame for easier comparison
pivoted_df = df.pivot(index='week', columns='client_name', values='duration_seconds')

# Calculate the percentage of total time spent on each client per week
total_time_per_week = pivoted_df.sum(axis=1)
percentage_per_client_per_week = (pivoted_df.div(total_time_per_week, axis=0) * 100)

# Print the results
print(percentage_per_client_per_week)
