"""Investigation: This script investigates the weekly time distribution trends across clients over the last 30 days and compares these trends to the target allocations. It calculates the total time spent on each client per week, pivots the dataframe for easier comparison, and then calculates the percentage of total time spent on each client per week.
Generated: 20260306_052054 UTC
"""

import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds, entries_to_dataframe

df = entries_to_dataframe(query_entries(days=30))
# Calculate total time spent on each client per week
client_weekly_time = df.groupby(['client_name', pd.Grouper(key='start', freq='W')])['duration_seconds'].sum().reset_index()
# Pivot the dataframe for easier comparison
pivoted_df = client_weekly_time.pivot(index='start', columns='client_name', values='duration_seconds')
# Calculate percentage of total time spent on each client per week
percentage_df = pivoted_df.div(pivoted_df.sum(axis=1), axis=0).fillna(0) * 100
print(percentage_df)