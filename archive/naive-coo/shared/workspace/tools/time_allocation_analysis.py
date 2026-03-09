"""Investigation: This script refines the investigation strategy by prioritizing robust error handling and troubleshooting mechanisms. It calculates total time spent on each client, identifies clients with significant deviations from target allocations, and attempts to calculate average session duration for each client while handling potential errors.
Generated: 20260305_200951 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent entries
entries = query_entries(days=30)

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate total time spent on each client
client_times = df.groupby('client_name')['duration_seconds'].sum()

# Identify clients with significant deviations from target allocations
target_allocations = {'STAR': 0.55, 'BBOY': 0.2, 'SEIFUKU': 0.15, 'BOJ': 0.1}
deviations = {}
for client, time in client_times.items():
    if client in target_allocations:
        deviation = abs(time - target_allocations[client] * df['duration_seconds'].sum())
        deviations[client] = deviation

# Print clients with significant deviations
print('Clients with significant deviations from target allocations:')
for client, deviation in deviations.items():
    print(f'{client}: {deviation}')

# Implement robust error handling and troubleshooting mechanisms
try:
    # Attempt to calculate average session duration for each client
    avg_session_durations = df.groupby('client_name')['duration_seconds'].mean()
    print('Average session durations:')
    print(avg_session_durations)
except Exception as e:
    print(f'Error: {e}')
