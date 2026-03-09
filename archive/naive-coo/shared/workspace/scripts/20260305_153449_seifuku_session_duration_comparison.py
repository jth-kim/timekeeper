"""Investigation: This script investigates the factors contributing to SEIFUKU's high average session duration compared to other clients and assesses its impact on overall time allocation against target priorities. It calculates the average session duration for each client, compares SEIFUKU's average to other clients', and prints the difference.
Generated: 20260305_153449 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent entries
entries = query_entries(days=14)

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate average session duration for each client
avg_durations = df.groupby('client_name')['duration_seconds'].mean()

# Print the average session durations
print(avg_durations)

# Compare SEIFUKU's average session duration to other clients
seifuku_avg = avg_durations['SEIFUKU']
other_clients_avg = avg_durations.drop('SEIFUKU').mean()

# Print the comparison
print(f'SEIFUKU average session duration: {seifuku_avg} seconds')
print(f'Other clients average session duration: {other_clients_avg} seconds')

# Calculate the difference between SEIFUKU's average and other clients' average
difference = seifuku_avg - other_clients_avg

# Print the difference
print(f'Difference: {difference} seconds')
