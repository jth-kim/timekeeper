"""Investigation: This script analyzes the daily time allocation patterns across different clients over the past two weeks and compares these patterns to the target allocations. It first queries the time-tracking data for the last 14 days, then groups the data by day and client, summing the duration for each group. The actual allocations are calculated as the proportion of total duration spent on each client. Finally, it prints the daily time allocation patterns, actual allocations, and target allocations for comparison.
Generated: 20260304_224107 UTC
"""

import pandas as pd
from supabase_helper import query_entries

df = pd.DataFrame(query_entries(days=14))
# Ensure 'start' column is of datetime type for grouper function
df['start'] = pd.to_datetime(df['start'])

daily_client_time = df.groupby([pd.Grouper(key='start', freq='D'), 'client_name'])['duration'].sum().reset_index()
print(daily_client_time)

target_allocations = {'STAR': 0.55, 'BBOY': 0.2, 'SEIFUKU': 0.15, 'BOJ': 0.1}
actual_allocations = daily_client_time.groupby('client_name')['duration'].sum() / daily_client_time['duration'].sum()
print(actual_allocations)
print(target_allocations)