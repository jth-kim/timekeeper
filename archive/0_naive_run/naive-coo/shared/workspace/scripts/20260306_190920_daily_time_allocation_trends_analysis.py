"""Investigation: This script investigates daily time allocation trends across clients over the last week and compares these trends to the target allocations, providing insights into potential imbalances or patterns in time allocation.
Generated: 20260306_190920 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query entries for the last week
entries = query_entries(days=7)

# Convert entries to a DataFrame
df = entries_to_dataframe(entries)

# Calculate daily time allocation trends across clients
daily_trends = df.groupby([pd.Grouper(key='start', freq='D'), 'client_name'])['duration_seconds'].sum().reset_index()

# Pivot the DataFrame for easier comparison
pivoted_df = daily_trends.pivot(index='start', columns='client_name', values='duration_seconds')

# Calculate the percentage of total time spent on each client per day
percentage_df = pivoted_df.div(pivoted_df.sum(axis=1), axis=0) * 100

# Print the results
print(percentage_df)
