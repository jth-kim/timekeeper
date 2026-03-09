"""Investigation: This script investigates the weekly time distribution trends across clients over the last 30 days and compares these trends to the target allocations. It aims to understand how time allocation varies by client and week, providing insights into potential imbalances or patterns that could inform adjustments to priorities or alert thresholds.
Generated: 20260306_183901 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent entries
recent_entries = query_entries(days=30)

# Convert to DataFrame
df = entries_to_dataframe(recent_entries)

# Calculate weekly time distribution trends
weekly_trends = df.groupby('client_name')['duration_seconds'].sum().reset_index()

# Calculate target allocations
target_allocations = {'STAR': 0.55, 'BBOY': 0.2, 'SEIFUKU': 0.15, 'BOJ': 0.1}

# Compare trends to target allocations
comparison = pd.DataFrame({'client_name': list(target_allocations.keys()), 'target_allocation': list(target_allocations.values())})
comparison = comparison.merge(weekly_trends, on='client_name', how='left')

# Print findings
print(comparison)
