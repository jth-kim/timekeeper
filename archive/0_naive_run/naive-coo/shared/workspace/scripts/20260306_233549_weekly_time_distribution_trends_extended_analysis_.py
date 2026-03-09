"""Investigation: This script investigates the weekly time distribution trends across clients over an extended period of 90 days and compares these trends to the target allocations, providing a broader perspective on time allocation patterns.
Generated: 20260306_233549 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query entries for the last 90 days
entries = query_entries(days=90)

# Convert entries to a DataFrame
df = pd.DataFrame(entries)

# Calculate weekly time distribution trends across clients
weekly_trends = df.groupby('client_name')['duration'].sum().reset_index()

# Compare trends to target allocations
target_allocations = {'STAR': 0.55, 'BBOY': 0.2, 'SEIFUKU': 0.15, 'BOJ': 0.1}
comparison = weekly_trends.merge(pd.DataFrame(list(target_allocations.items()), columns=['client_name', 'target_allocation']), on='client_name')

# Print the comparison
print(comparison)
