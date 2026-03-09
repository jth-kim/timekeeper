"""Investigation: This script analyzes the daily time allocation patterns across different clients over the past two weeks and compares these patterns to the target allocations. It helps in understanding how the Sovereign's time allocation has been distributed among various clients and identifies any deviations from the intended priorities.
Generated: 20260304_222745 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query entries for the last 14 days
entries = query_entries(days=14)

# Convert entries to a Pandas DataFrame for easier analysis
df = pd.DataFrame(entries)

# Calculate total time spent on each client per day
daily_client_time = df.groupby([pd.Grouper(key='start', freq='D'), 'client_name'])['duration'].sum().reset_index()

# Pivot the data to have clients as columns and days as rows
pivoted_df = daily_client_time.pivot(index='start', columns='client_name', values='duration')

# Calculate the average daily time allocation for each client over the past two weeks
average_daily_allocation = pivoted_df.mean()

# Print the average daily time allocation for each client
print(average_daily_allocation)

# Compare the average daily allocations to the target allocations
target_allocations = {'STAR': 0.55, 'BBOY': 0.2, 'SEIFUKU': 0.15, 'BOJ': 0.1}
for client, target in target_allocations.items():
    if client in average_daily_allocation:
        print(f'{client} average daily allocation: {average_daily_allocation[client]} hours, Target: {target * 24} hours')
    else:
        print(f'No data for {client}')
