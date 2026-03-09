"""Investigation: This script investigates the weekly time distribution trends across clients over an extended period of 120 days and compares these trends to the target allocations. It calculates the total time spent on each client per week, pivots the dataframe for easier comparison, and then calculates the percentage of total time spent on each client per week.
Generated: 20260306_113101 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

days = 120
entries = query_entries(days=days)
dataframe = entries_to_dataframe(entries)

total_time_per_client = dataframe.groupby('client_name')['duration_seconds'].sum()
pivot_table = dataframe.pivot_table(index='client_name', columns='week', values='duration_seconds', aggfunc='sum')

print("Total time per client over {} days:").format(days)
print(total_time_per_client)
print(\n"Pivot table of weekly time distribution:\n")
print(pivot_table)