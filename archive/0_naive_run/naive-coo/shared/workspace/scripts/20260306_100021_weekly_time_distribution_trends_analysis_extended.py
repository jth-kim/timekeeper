"""Investigation: This script investigates the weekly time distribution trends across clients over an extended period of 90 days and compares these trends to the target allocations. It calculates the total time spent on each client per week, pivots the data for easier comparison, and then calculates the percentage of total time spent on each client per week. The results are printed to stdout in a clear format, providing insights into how time allocation varies across different clients over time.
Generated: 20260306_100021 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data for the last 90 days
entries = query_entries(days=90)

# Convert entries to a DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate total time spent on each client per week
df['week'] = pd.to_datetime(df['start']).dt.isocalendar().week
weekly_time_df = df.groupby(['client_name', 'week'])['duration_seconds'].sum().reset_index()

# Pivot the DataFrame for easier comparison
pivoted_df = weekly_time_df.pivot(index='week', columns='client_name', values='duration_seconds')

# Calculate the percentage of total time spent on each client per week
total_time_per_week = pivoted_df.sum(axis=1)
percentage_df = (pivoted_df / total_time_per_week) * 100

# Print the results
print(percentage_df)

# Save the figure to /data/workspace/results/
import matplotlib.pyplot as plt
plt.figure(figsize=(10,6))
plt.plot(percentage_df.index, percentage_df['SEIFUKU'], label='SEIFUKU')
plt.plot(percentage_df.index, percentage_df['STAR'], label='STAR')
plt.plot(percentage_df.index, percentage_df['BBOY'], label='BBOY')
plt.legend()
plt.xlabel('Week')
plt.ylabel('Percentage of Total Time')
plt.title('Weekly Time Distribution Trends Across Clients')
plt.savefig('/data/workspace/results/weekly_time_distribution_trends.png')
