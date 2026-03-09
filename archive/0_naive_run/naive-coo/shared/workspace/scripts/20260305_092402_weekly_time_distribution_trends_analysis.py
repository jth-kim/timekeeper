"""Investigation: This script analyzes the weekly time distribution trends across clients over the last 30 days and compares these trends to the target allocations. It calculates the total time spent on each client and divides it by the total possible time in the period (30 days * 24 hours * 60 minutes * 60 seconds) to get the percentage allocation for each client.
Generated: 20260305_092402 UTC
"""

import pandas as pd
from supabase_helper import query_entries

days = 30
entries = query_entries(days=days)
if not entries:
    print("No entries found.")
    exit()

df = pd.DataFrame(entries)
# Ensure 'start' column is datetime for grouping by time frequencies
df['start'] = pd.to_datetime(df['start'])

target_allocations = {"STAR": 0.55, "BBOY": 0.2, "SEIFUKU": 0.15, "BOJ": 0.1}
client_time_allocations = {}
for client in target_allocations.keys():
    client_entries = df[df['client_name'] == client]
    total_seconds = client_entries['duration'].apply(lambda x: int(x.total_seconds())).sum()
    client_time_allocations[client] = total_seconds / (days * 24 * 60 * 60)

print("Weekly time distribution trends across clients:")
for client, allocation in client_time_allocations.items():
    print(f"{client}: {allocation:.2%}")
print("\nTarget allocations:")
for client, target in target_allocations.items():
    print(f"{client}: {target:.2%}")