"""Investigation: This script investigates the weekly time distribution trends across clients over the last 30 days and compares these trends to the target allocations. It calculates total hours spent on each client per week, pivots the dataframe for easier comparison, and then calculates the percentage of total time spent on each client per week.
Generated: 20260306_081856 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data for the last 30 days
entries = query_entries(days=30)

# Convert entries to a DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate total hours spent on each client per week
df['week'] = pd.to_datetime(df['start']).dt.to_period('W')
weekly_hours = df.groupby(['client_name', 'week'])['duration_seconds'].sum().reset_index()

# Pivot the dataframe for easier comparison
pivoted_df = weekly_hours.pivot(index='week', columns='client_name', values='duration_seconds')

# Calculate the percentage of total time spent on each client per week
total_time_per_week = pivoted_df.sum(axis=1)
percentage_per_client = pivoted_df.div(total_time_per_week, axis=0) * 100

# Print the results in a clear format
print('Weekly Time Distribution Trends Across Clients:')
print(pivoted_df)
print('\
Percentage of Total Time Spent on Each Client Per Week:')
print(percentage_per_client)

# Compare trends to target allocations
target_allocations = {'STAR': 0.55, 'BBOY': 0.2, 'SEIFUKU': 0.15, 'BOJ': 0.1}
for client, target in target_allocations.items():
    actual_percentage = percentage_per_client[client].mean()
    print(f'Client: {client}, Target Allocation: {target*100}%, Actual Percentage: {actual_percentage:.2f}%')
