"""Investigation: This script analyzes the weekly time distribution trends across clients over the last 30 days and compares these trends to the target allocations. It calculates the total time spent on each client per week, pivots the dataframe for easier comparison, and then calculates the percentage of total time spent on each client per week.
Generated: 20260305_223702 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

days = 30
entries = query_entries(days=days)
df = entries_to_dataframe(entries)

target_allocations = {"STAR": 0.55, "BBOY": 0.2, "SEIFUKU": 0.15, "BOJ": 0.1}

total_time = df['duration_seconds'].sum()
client_times = df.groupby('client_name')['duration_seconds'].sum().to_dict()

for client, target in target_allocations.items():
    actual_allocation = client_times.get(client, 0) / total_time
    print(f"Client: {client}, Target Allocation: {target:.2f}, Actual Allocation: {actual_allocation:.2f}")