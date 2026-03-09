"""Investigation: This script investigates the weekly time distribution trends across clients over an extended period of 150 days and compares these trends to the target allocations. It calculates the total time spent on each client per week, pivots the DataFrame for easier comparison, and then calculates the percentage of total time spent on each client per week.
Generated: 20260306_170147 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query entries for the last 150 days
entries = query_entries(days=150)

# Convert entries to a DataFrame
df = pd.DataFrame(entries)

# Calculate total time spent on each client per week
weekly_time = df.groupby('client_name')['duration'].sum().reset_index()

# Pivot the DataFrame for easier comparison
pivoted_df = weekly_time.pivot(index='client_name', columns='week', values='duration')

# Calculate the percentage of total time spent on each client per week
percentage_df = pivoted_df.div(pivoted_df.sum(axis=0), axis=1) * 100

# Print the results
print(percentage_df)
