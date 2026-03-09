"""Investigation: This script analyzes the weekly time distribution trends across clients over the last 30 days and compares these trends to the target allocations. It provides insights into how time allocation varies by client and week, helping to identify potential imbalances or trends that could inform adjustments to achieve a more balanced time allocation.
Generated: 20260305_083131 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query recent entries
entries = query_entries(days=30)

# Convert to DataFrame
df = pd.DataFrame(entries)

# Calculate weekly time distribution for each client
weekly_time_allocations = {}
for client in df['client_name'].unique():
    client_df = df[df['client_name'] == client]
    weekly_time_allocation = client_df.groupby(client_df['start'].dt.to_period('W'))['duration'].sum()
    weekly_time_allocations[client] = weekly_time_allocation

# Compare to target allocations
target_allocations = {'STAR': 0.55, 'BBOY': 0.2, 'SEIFUKU': 0.15, 'BOJ': 0.1}
for client, allocation in weekly_time_allocations.items():
    print(f'Client: {client}, Weekly Time Allocation: {allocation}, Target Allocation: {target_allocations.get(client, 0)}')
