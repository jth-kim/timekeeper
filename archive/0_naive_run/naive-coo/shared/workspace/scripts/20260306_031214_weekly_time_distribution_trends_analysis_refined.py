"""Investigation: This script investigates the weekly time distribution trends across clients over the last 30 days and compares these trends to the target allocations. It calculates the total time spent on each client per week, pivots the dataframe for easier comparison, and then calculates the percentage of total time spent on each client per week.
Generated: 20260306_031214 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

df = entries_to_dataframe(query_entries(days=30))
# Calculate total time spent on each client per week
total_time_per_client_per_week = df.groupby(['client_name', pd.Grouper(key='start', freq='W')])['duration_seconds'].sum().reset_index()
# Pivot the dataframe for easier comparison
total_time_per_client_per_week_pivot = total_time_per_client_per_week.pivot(index='start', columns='client_name', values='duration_seconds')
# Calculate the percentage of total time spent on each client per week
total_time_per_week = total_time_per_client_per_week_pivot.sum(axis=1)
time_percentage_per_client_per_week = (total_time_per_client_per_week_pivot.div(total_time_per_week, axis=0) * 100).round(2)
# Print the results
cols = ['STAR', 'BBOY', 'SEIFUKU']
print(time_percentage_per_client_per_week[cols])