"""Investigation: This script calculates the actual hour totals for each client over the last 30 days and compares them to the target allocations, providing insights into potential imbalances in time allocation.
Generated: 20260307_161319 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

df = entries_to_dataframe(query_entries(days=30))
# Calculate total hours for each client
client_hours = df.groupby('client_name')['duration_seconds'].sum() / 3600
print(client_hours)

target_allocations = {'STAR': 0.55, 'BBOY': 0.2, 'SEIFUKU': 0.15, 'BOJ': 0.1}
actual_allocations = client_hours / client_hours.sum()
print(actual_allocations)

discrepancies = actual_allocations - pd.Series(target_allocations)
print(discrepancies)