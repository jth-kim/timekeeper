"""Investigation: This script calculates the hourly totals for each client over the last week and compares these totals to the target allocations. It provides insights into potential imbalances in time allocation and informs adjustments to alert thresholds if necessary.
Generated: 20260307_135055 UTC
"""


import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds

# Query entries for the last week
entries = query_entries(days=7)

# Convert entries to a DataFrame
df = pd.DataFrame(entries)

# Calculate total hours for each client
client_hours = df.groupby('client_name')['duration'].apply(lambda x: sum(parse_duration_seconds(d) for d in x) / 3600).to_dict()

# Print the hourly totals for each client
print(client_hours)

# Compare the hourly totals to the target allocations
target_allocations = {'STAR': 0.55, 'BBOY': 0.2, 'SEIFUKU': 0.15, 'BOJ': 0.1}
total_hours = sum(client_hours.values())
for client, hours in client_hours.items():
    print(f'{client}: {hours} hours ({hours / total_hours * 100:.2f}% of total) vs target {target_allocations.get(client, 0) * 100:.2f}%')
