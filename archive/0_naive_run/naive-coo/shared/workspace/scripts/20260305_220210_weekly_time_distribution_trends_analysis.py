"""Investigation: This script investigates the weekly time distribution trends across clients over the last 30 days and compares these trends to the target allocations. It calculates the total time spent on each client per week, pivots the dataframe for easier comparison, and then calculates the percentage of total time spent on each client per week.
Generated: 20260305_220210 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent entries
entries = query_entries(days=30)

# Convert entries to DataFrame
df = entries_to_dataframe(entries)

# Calculate total time spent on each client per week
weekly_time_spent = df.groupby(['client_name', pd.Grouper(key='start', freq='W')])['duration_seconds'].sum().reset_index()

# Pivot the dataframe for easier comparison
pivoted_df = weekly_time_spent.pivot(index='start', columns='client_name', values='duration_seconds')

# Calculate the percentage of total time spent on each client per week
total_time_per_week = pivoted_df.sum(axis=1)
percentage_per_client = pivoted_df.div(total_time_per_week, axis=0) * 100

# Print the results
print(percentage_per_client)

# Compare to target allocations
target_allocations = {'STAR': 0.55, 'BBOY': 0.2, 'SEIFUKU': 0.15, 'BOJ': 0.1}
for client, target in target_allocations.items():
    print(f'Target allocation for {client}: {target:.2%}')
    if client in percentage_per_client.columns:
        actual_allocation = percentage_per_client[client].mean()
        print(f'Actual allocation for {client}: {actual_allocation:.2%}')
        if abs(actual_allocation - target) > 0.1:  # arbitrary threshold
            print(f'Warning: Actual allocation for {client} deviates from target by more than 10%')
    else:
        print(f'No data available for client {client}')
