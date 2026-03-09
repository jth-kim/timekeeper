"""Investigation: This script calculates the actual hour totals for each client over the last week and compares these totals to the target allocations, providing insights into potential imbalances in time allocation.
Generated: 20260306_214226 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data
entries = query_entries(days=7)

# Convert entries to a DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate total hours for each client
client_hours = df.groupby('client_name')['duration_seconds'].sum() / 3600

# Define target allocations
target_allocations = {
    'STAR': 0.55,
    'BBOY': 0.2,
    'SEIFUKU': 0.15,
    'BOJ': 0.1
}

# Calculate total hours across all clients
total_hours = client_hours.sum()

# Compare actual hour totals to target allocations
for client, hours in client_hours.items():
    target_hours = total_hours * target_allocations.get(client, 0)
    print(f'Client: {client}, Actual Hours: {hours:.2f}, Target Hours: {target_hours:.2f}')
