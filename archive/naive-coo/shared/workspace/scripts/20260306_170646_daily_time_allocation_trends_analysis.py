"""Investigation: This script investigates daily time allocation trends across clients over the last 14 days and compares these trends to the target allocations, providing insights into potential imbalances or patterns in time allocation.
Generated: 20260306_170646 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

df = entries_to_dataframe(query_entries(days=14))
# Calculate daily time allocation for each client
daily_allocations = df.groupby([pd.Grouper(key='start', freq='D'), 'client_name'])['duration_seconds'].sum().reset_index()
# Pivot dataframe for easier comparison
pivoted_df = daily_allocations.pivot(index='start', columns='client_name', values='duration_seconds')
# Calculate percentage of total time spent on each client per day
percentages = pivoted_df.div(pivoted_df.sum(axis=1), axis=0).fillna(0) * 100
print(percentages)