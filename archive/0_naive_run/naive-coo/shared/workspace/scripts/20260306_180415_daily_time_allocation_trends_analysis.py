"""Investigation: This script investigates daily time allocation trends across clients over the last 14 days and compares these trends to the target allocations, providing insights into potential imbalances or patterns in time allocation.
Generated: 20260306_180415 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query entries for the last 14 days
entries = query_entries(days=14)

# Convert entries to DataFrame
df = pd.DataFrame(entries)

# Ensure 'start' column is datetime
df['start'] = pd.to_datetime(df['start'])

# Calculate daily time allocation for each client
daily_allocation = df.groupby([pd.Grouper(key='start', freq='D'), 'client_name'])['duration'].sum().reset_index()

# Pivot DataFrame for easier comparison
pivoted_df = daily_allocation.pivot(index='start', columns='client_name', values='duration')

# Calculate percentage of total time spent on each client per day
percentage_df = pivoted_df.div(pivoted_df.sum(axis=1), axis=0)

# Print daily time allocation trends
print(percentage_df)

# Compare trends to target allocations
target_allocations = {'STAR': 0.55, 'BBOY': 0.2, 'SEIFUKU': 0.15, 'BOJ': 0.1}
for client, target in target_allocations.items():
    print(f'Daily time allocation trend for {client}: {percentage_df[client].mean()}')
    if abs(percentage_df[client].mean() - target) > 0.1:
        print(f'Warning: Daily time allocation for {client} deviates from target by more than 10%')
