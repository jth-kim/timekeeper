"""Investigation: This script investigates the weekly time distribution trends across clients over an extended period of 90 days and compares these trends to the target allocations. It calculates the total time spent on each client per week, pivots the dataframe for easier comparison, and then calculates the percentage of total time spent on each client per week.
Generated: 20260306_105012 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

days = 90
entries = query_entries(days=days)
df = entries_to_dataframe(entries)
# Calculate weekly time distribution trends across clients
trends = df.groupby([pd.Grouper(key='start', freq='W'), 'client_name'])['duration_seconds'].sum().reset_index()
# Compare trends to target allocations
star_target = 0.55 * (trends['duration_seconds'].sum())
bboy_target = 0.2 * (trends['duration_seconds'].sum())
seifuku_target = 0.15 * (trends['duration_seconds'].sum())
boj_target = 0.1 * (trends['duration_seconds'].sum())
targets = pd.DataFrame({'client_name': ['STAR', 'BBOY', 'SEIFUKU', 'BOJ'], 'target': [star_target, bboy_target, seifuku_target, boj_target]})
# Merge trends with targets for comparison
comparison = pd.merge(trends, targets, on='client_name')
print(comparison)