"""Investigation: This script investigates daily time allocation patterns across clients over the last 14 days and compares these patterns to the target allocations, providing insights into potential imbalances or trends in time allocation.
Generated: 20260307_042447 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

days = 14
entries = query_entries(days=days)
df = entries_to_dataframe(entries)

daily_allocations = df.groupby([pd.Grouper(key='start', freq='D'), 'client_name'])['duration_seconds'].sum().reset_index()
daily_allocations.columns = ['date', 'client', 'total_seconds']

targets = {'STAR': 0.55, 'BBOY': 0.2, 'SEIFUKU': 0.15, 'BOJ': 0.1}

for client, target in targets.items():
    client_df = daily_allocations[daily_allocations['client'] == client]
    client_df['target_seconds'] = client_df['total_seconds'] * target
    print(f'Daily time allocation for {client} over the last {days} days:')
    print(client_df)
