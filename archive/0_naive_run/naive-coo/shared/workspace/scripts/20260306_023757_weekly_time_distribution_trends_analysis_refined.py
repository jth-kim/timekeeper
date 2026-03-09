"""Investigation: This script investigates the weekly time distribution trends across clients over the last 30 days and compares these trends to the target allocations. It calculates the total time spent on each client per week, pivots the dataframe for easier comparison, and then calculates the percentage of total time spent on each client per week. The results are printed to stdout in a clear format.
Generated: 20260306_023757 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query the time-tracking data for the last 30 days
entries = query_entries(days=30)

# Convert the entries to a DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate the total time spent on each client per week
weekly_time_spent = df.groupby('client_name')['duration_seconds'].sum().reset_index()

# Pivot the dataframe for easier comparison
pivoted_df = weekly_time_spent.pivot(index='client_name', values='duration_seconds')

# Calculate the percentage of total time spent on each client per week
percentage_time_spent = pivoted_df.div(pivoted_df.sum(axis=0), axis=1) * 100

# Print the results
print('Weekly Time Distribution Trends Across Clients:')
print(percentage_time_spent)

# Compare the trends to the target allocations
target_allocations = {'STAR': 0.55, 'BBOY': 0.2, 'SEIFUKU': 0.15, 'BOJ': 0.1}
for client, target in target_allocations.items():
    actual_percentage = percentage_time_spent.loc[client].sum()
    if abs(actual_percentage - target) > 0.05:
        print(f'Warning: {client} is deviating from its target allocation by more than 5%')
