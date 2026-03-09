"""Investigation: This script investigates the weekly time distribution trends across clients over the last 30 days and compares these trends to the target allocations, providing insights into potential imbalances or patterns in time allocation.
Generated: 20260306_204252 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

df = entries_to_dataframe(query_entries(days=30))
# Calculate total time spent on each client per week
weekly_totals = df.groupby([pd.Grouper(key='start', freq='W'), 'client_name'])['duration_seconds'].sum().reset_index()
# Pivot the dataframe for easier comparison
pivoted_df = weekly_totals.pivot(index='start', columns='client_name', values='duration_seconds')
# Calculate the percentage of total time spent on each client per week
percentage_df = pivoted_df.div(pivoted_df.sum(axis=1), axis=0).fillna(0) * 100
print(percentage_df)