"""Investigation: This script investigates the discrepancy between actual hour totals for each client and target allocations over the last week, aiming to understand potential imbalances in time allocation.
Generated: 20260307_085106 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

df = entries_to_dataframe(query_entries(days=7))
# Calculate actual hour totals for each client
actual_hours = df.groupby('client_name')['duration_seconds'].sum() / 3600
print(actual_hours)

target_allocations = {'STAR': 0.55, 'BBOY': 0.2, 'SEIFUKU': 0.15, 'BOJ': 0.1}
# Calculate discrepancy between actual and target allocations
discrepancy = (actual_hours / actual_hours.sum()) - pd.Series(target_allocations)
print(discrepancy)