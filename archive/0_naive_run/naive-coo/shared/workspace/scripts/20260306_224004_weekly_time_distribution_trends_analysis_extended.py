"""Investigation: This script investigates weekly time distribution trends across clients over the last 30 days and compares these trends to the target allocations, providing insights into potential imbalances or patterns in time allocation.
Generated: 20260306_224004 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

df = entries_to_dataframe(query_entries(days=30))
# Calculate total time spent on each client per week
weekly_totals = df.groupby('client_name')['duration_seconds'].sum().reset_index()
# Pivot the dataframe for easier comparison
pivoted_df = weekly_totals.pivot(index='client_name', columns='week', values='duration_seconds')
# Calculate the percentage of total time spent on each client per week
percentages = pivoted_df.div(pivoted_df.sum(axis=0), axis=1).fillna(0) * 100
print(percentages)