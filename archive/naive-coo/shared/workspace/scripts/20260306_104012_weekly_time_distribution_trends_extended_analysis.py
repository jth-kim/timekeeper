"""Investigation: This script investigates the weekly time distribution trends across clients over an extended period of 90 days and compares these trends to the target allocations. It calculates the total time spent on each client per week, pivots the dataframe for easier comparison, and then calculates the percentage of total time spent on each client per week. The results are printed to stdout in a clear format, providing insights into how time allocation varies across different clients over time.
Generated: 20260306_104012 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query the last 90 days of entries
entries = query_entries(days=90)

# Convert the entries to a DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate the total time spent on each client per week
weekly_time_df = df.groupby('client_name')['duration_seconds'].sum().reset_index()

# Pivot the dataframe for easier comparison
pivoted_df = weekly_time_df.pivot(index='client_name', columns='week', values='duration_seconds')

# Calculate the percentage of total time spent on each client per week
percentage_df = pivoted_df.div(pivoted_df.sum(axis=0), axis=1) * 100

# Print the results in a clear format
print(percentage_df)
