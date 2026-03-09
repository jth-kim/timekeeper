"""Investigation: This script investigates the primary factors contributing to discrepancies between actual and target time allocations across clients. It calculates actual hour totals for each client, compares them to target allocations, identifies significant discrepancies, and proposes adjustments to alert thresholds to better support the Sovereign's productivity.
Generated: 20260307_152311 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query recent entries (e.g., last 30 days)
entries = query_entries(days=30)

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate actual hour totals for each client
actual_totals = df.groupby('client_name')['duration_seconds'].sum() / 3600

# Compare to target allocations
target_allocations = {'STAR': 0.55, 'BBOY': 0.2, 'SEIFUKU': 0.15, 'BOJ': 0.1}
discrepancies = actual_totals - pd.Series(target_allocations)

# Identify clients with significant discrepancies
significant_discrepancies = discrepancies[abs(discrepancies) > 0.25]

# Print findings and propose adjustments to alert thresholds
print('Significant discrepancies in time allocation:')
print(significant_discrepancies)
print('Proposed adjustments to alert thresholds:')
for client, discrepancy in significant_discrepancies.items():
    if discrepancy > 0:
        print(f'Decrease alert threshold for {client} by {abs(discrepancy)} hours')
    else:
        print(f'Increase alert threshold for {client} by {abs(discrepancy)} hours')
