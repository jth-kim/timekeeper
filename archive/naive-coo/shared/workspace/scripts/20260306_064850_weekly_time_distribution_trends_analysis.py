"""Investigation: This script investigates the weekly time distribution trends across clients over the last 30 days and compares these trends to the target allocations. It calculates the total time spent on each client per week, pivots the dataframe for easier comparison, and then calculates the percentage of total time spent on each client per week. The findings are printed in a clear format, allowing for easy identification of potential imbalances in time allocation.
Generated: 20260306_064850 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data for the last 30 days
entries = query_entries(days=30)

# Convert entries to a DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate total time spent on each client per week
weekly_time_df = df.groupby('client_name')['duration_seconds'].sum().reset_index()

# Pivot the dataframe for easier comparison
pivoted_df = weekly_time_df.pivot(index='client_name', columns='week', values='duration_seconds')

# Calculate the percentage of total time spent on each client per week
percentage_df = pivoted_df.div(pivoted_df.sum(axis=0), axis=1) * 100

# Print findings in a clear format
print('Weekly Time Distribution Trends Across Clients:')
print(percentage_df)

# Compare trends to target allocations
target_allocations = {
    'STAR': 0.55,
    'BBOY': 0.2,
    'SEIFUKU': 0.15,
    'BOJ': 0.1
}

for client, target in target_allocations.items():
    actual_percentage = percentage_df.loc[client].mean()
    print(f'Client: {client}, Target Allocation: {target*100}%, Actual Percentage: {actual_percentage:.2f}%')
