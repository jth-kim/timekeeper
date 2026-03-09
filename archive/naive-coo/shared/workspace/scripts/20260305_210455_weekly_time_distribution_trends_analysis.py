"""Investigation: This script investigates the weekly time distribution trends across clients over the last 30 days and compares these trends to the target allocations. It calculates the total time spent on each client per week, pivots the DataFrame for easier comparison, and then calculates the percentage of total time spent on each client per week.
Generated: 20260305_210455 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query entries for the last 30 days
entries = query_entries(days=30)

# Convert entries to a DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate total time spent on each client per week
weekly_time_spent = df.groupby('client_name')['duration_seconds'].sum().reset_index()

# Pivot the DataFrame for easier comparison
pivoted_df = weekly_time_spent.pivot(index='client_name', values='duration_seconds')

# Calculate the percentage of total time spent on each client per week
total_time_per_week = pivoted_df.sum(axis=1)
percentage_per_client = (pivoted_df.div(total_time_per_week, axis=0)).fillna(0) * 100

# Print the results
print('Weekly Time Distribution Trends:')
print(pivoted_df)
print('\
Percentage of Total Time per Client:')
print(percentage_per_client)

# Compare to target allocations
target_allocations = {'STAR': 0.55, 'BBOY': 0.2, 'SEIFUKU': 0.15, 'BOJ': 0.1}
for client, target in target_allocations.items():
    actual_percentage = percentage_per_client.loc[client].sum()
    print(f'Client {client}: Target={target:.2f}, Actual={actual_percentage:.2f}')
