"""Investigation: This script investigates the weekly time distribution trends across clients over the last 30 days and compares these trends to the target allocations, providing insights into potential imbalances in time allocation.
Generated: 20260305_090325 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query entries for the last 30 days
entries = query_entries(days=30)

# Convert entries to DataFrame
df = pd.DataFrame(entries)

# Ensure 'start' column is datetime
df['start'] = pd.to_datetime(df['start'])

# Group by client and week, calculate total time
weekly_time_df = df.groupby([pd.Grouper(key='start', freq='W'), 'client_name'])['duration'].sum().reset_index()

# Pivot to get weekly time for each client
pivoted_df = weekly_time_df.pivot(index='start', columns='client_name', values='duration')

# Calculate target allocations
target_allocations = {
    'STAR': 0.55,
    'BBOY': 0.2,
    'SEIFUKU': 0.15,
    'BOJ': 0.1
}

# Compare actual time distribution to target allocations
for client, target_allocation in target_allocations.items():
    actual_time = pivoted_df[client].sum()
    print(f'Client: {client}, Actual Time: {actual_time}, Target Allocation: {target_allocation}')
