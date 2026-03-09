"""Investigation: This script investigates the weekly time distribution trends across clients over the last 30 days and compares these trends to the target allocations. It calculates the total time spent on each client per week, pivots the dataframe for easier comparison, and then calculates the percentage of total time spent on each client per week.
Generated: 20260305_191557 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

days = 30
entries = query_entries(days=days)
dataframe = entries_to_dataframe(entries)

dataframe['start'] = pd.to_datetime(dataframe['start'])
trends = dataframe.groupby([pd.Grouper(key='start', freq='W'), 'client_name'])['duration_seconds'].sum().reset_index()
targets = {'STAR': 0.55, 'BBOY': 0.2, 'SEIFUKU': 0.15, 'BOJ': 0.1}

trends['target_allocation'] = trends['client_name'].map(targets)
trends['actual_allocation'] = trends['duration_seconds'] / trends['duration_seconds'].sum()

difference = trends['actual_allocation'] - trends['target_allocation']
print(difference)