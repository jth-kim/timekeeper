"""Investigation: This script investigates weekly time distribution trends across clients over an extended period and compares these trends to target allocations, providing a broader perspective on time allocation patterns.
Generated: 20260306_231805 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

days = 60
entries = query_entries(days=days)
df = entries_to_dataframe(entries)
# Calculate total time spent on each client per week
total_time_per_week = df.groupby('client_name')['duration_seconds'].sum().reset_index()
# Pivot the dataframe for easier comparison
total_time_pivot = total_time_per_week.pivot(index='client_name', columns='week', values='duration_seconds')
# Calculate percentage of total time spent on each client per week
total_time_percentage = (total_time_pivot / total_time_pivot.sum()) * 100
print(total_time_percentage)