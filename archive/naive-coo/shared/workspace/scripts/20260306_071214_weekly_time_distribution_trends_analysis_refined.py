"""Investigation: This script investigates the weekly time distribution trends across clients over the last 30 days and compares these trends to the target allocations. It calculates the total time spent on each client per week, pivots the dataframe for easier comparison, and then calculates the percentage of total time spent on each client per week.
Generated: 20260306_071214 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query entries for the last 30 days
entries = query_entries(days=30)

# Convert entries to a DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate total time spent on each client per week
weekly_time_spent = df.groupby('client_name')['duration_seconds'].sum().reset_index()

# Pivot the dataframe for easier comparison
pivoted_df = weekly_time_spent.pivot(index='client_name', columns='week', values='duration_seconds')

# Calculate percentage of total time spent on each client per week
percentage_df = pivoted_df.div(pivoted_df.sum(axis=0), axis=1) * 100

# Print the results in a clear format
print(percentage_df)

# Save the figure to /data/workspace/results/
import matplotlib.pyplot as plt
percentage_df.plot(kind='bar')
plt.savefig('/data/workspace/results/weekly_time_distribution_trends.png')
