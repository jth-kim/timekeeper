"""Investigation: This script investigates the daily time allocation trends for each client over the last 14 days and compares these trends to the target allocations. It calculates the total time spent on each client per day, resamples the data to get the daily mean, and prints the results along with the target allocations.
Generated: 20260307_003321 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

days = 14
entries = query_entries(days=days)
dataframe = entries_to_dataframe(entries)

total_seconds_per_day = dataframe.groupby('client_name')['duration_seconds'].sum().reset_index()
total_seconds_per_day['date'] = pd.to_datetime(total_seconds_per_day.index)
total_seconds_per_day.set_index('date', inplace=True)

daily_trends = total_seconds_per_day.resample('D').mean()

target_allocations = {'STAR': 0.55, 'BBOY': 0.2, 'SEIFUKU': 0.15, 'BOJ': 0.1}

print(daily_trends)
print(target_allocations)