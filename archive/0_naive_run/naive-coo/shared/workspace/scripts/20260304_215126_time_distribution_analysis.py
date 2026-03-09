"""Investigation: This script analyzes the distribution of time spent on different clients over the last week and compares it to the target allocations. It calculates the total time spent on each client, converts it to a percentage of the total time, and prints the results. Then, it compares these percentages to the target allocations and prints the comparison.
Generated: 20260304_215126 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query entries for the last week
entries = query_entries(days=7)

# Convert entries to a DataFrame
df = pd.DataFrame(entries)

# Calculate total time spent on each client
client_times = df.groupby('client_name')['duration'].sum()

# Calculate percentage of total time for each client
total_time = client_times.sum()
client_percentages = (client_times / total_time) * 100

# Print the results
print(client_percentages)

# Compare to target allocations
target_allocations = {'STAR': 0.55, 'BBOY': 0.2, 'SEIFUKU': 0.15, 'BOJ': 0.1}
for client, target in target_allocations.items():
    if client in client_percentages:
        print(f'{client}: {client_percentages[client]}% (target: {target*100}%)')
    else:
        print(f'{client}: 0% (target: {target*100}%)')
