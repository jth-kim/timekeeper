"""Investigation: This script calculates the actual hour totals for each client over the last 30 days, compares them to the target allocations, and prints the discrepancies. It aims to identify potential imbalances in time allocation and inform adjustments to alert thresholds.
Generated: 20260307_162124 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data
entries = query_entries(days=30)

# Convert entries to a DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate actual hour totals for each client
client_totals = df.groupby('client_name')['duration_seconds'].sum() / 3600

# Define target allocations
target_allocations = {
    'STAR': 0.55,
    'BBOY': 0.2,
    'SEIFUKU': 0.15,
    'BOJ': 0.1
}

# Calculate discrepancies between actual and target time allocations
discrepancies = client_totals - pd.Series(target_allocations) * df['duration_seconds'].sum() / 3600

# Print the results in a clear format
print('Actual hour totals for each client:')
print(client_totals)
print('
Target allocations:')
print(target_allocations)
print('
Discrepancies between actual and target time allocations:')
print(discrepancies)