"""Investigation: This script investigates the weekly time distribution trends across clients over the last 30 days and compares these trends to the target allocations. It calculates the total time spent on each client per week, pivots the dataframe for easier comparison, and then calculates the percentage of total time spent on each client per week.
Generated: 20260305_211144 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

df = entries_to_dataframe(query_entries(days=30))
# Group by client and calculate total time spent per week
total_time_per_week = df.groupby(['client_name', pd.Grouper(key='start', freq='W')])['duration_seconds'].sum().reset_index()
# Calculate percentage of total time spent on each client per week
total_time_per_week['percentage'] = total_time_per_week.groupby('start')['duration_seconds'].apply(lambda x: 100 * x / x.sum())
print(total_time_per_week)