"""Investigation: This script investigates the primary factors contributing to the discrepancy between actual and target time allocations across clients, specifically focusing on SEIFUKU's dominance. It calculates the total time spent on each client, compares these totals to the target allocations, and prints the discrepancies as percentages.
Generated: 20260307_163925 UTC
"""


import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds

# Query recent entries
entries = query_entries(days=14)

# Convert to DataFrame with proper types
df = pd.DataFrame(entries)
df['duration_seconds'] = df['duration'].apply(parse_duration_seconds)

# Calculate total time spent on each client
client_totals = df.groupby('client_name')['duration_seconds'].sum()

# Calculate target allocations
target_allocations = {
    'SEIFUKU': 0.15,
    'STAR': 0.55,
    'BBOY': 0.2,
    'BOJ': 0.1
}

# Compare actual totals to target allocations
discrepancies = {}
for client, total_seconds in client_totals.items():
    target_seconds = target_allocations[client] * sum(client_totals)
    discrepancy = (total_seconds - target_seconds) / target_seconds
    discrepancies[client] = discrepancy

# Print findings
print('Discrepancies between actual and target time allocations:')
for client, discrepancy in discrepancies.items():
    print(f'{client}: {discrepancy:.2%}')
