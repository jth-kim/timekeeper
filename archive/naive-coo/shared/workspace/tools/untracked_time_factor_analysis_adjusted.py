"""Investigation: This script investigates the factors contributing to the variability in untracked time between sessions and assesses their impact on overall time allocation against target priorities. It adjusts the dataframe to ensure the 'start' column is of the correct data type for analysis, calculates untracked time between sessions, and provides statistics on average and total untracked time.
Generated: 20260305_004849 UTC
"""

import pandas as pd
from supabase_helper import query_entries

df = pd.DataFrame(query_entries(days=14))
df['start'] = pd.to_datetime(df['start'])
df['stop'] = pd.to_datetime(df['stop'])

df.sort_values(by='start', inplace=True)
df['previous_stop'] = df['stop'].shift(1)
df['untracked_time'] = (df['start'] - df['previous_stop']).dt.total_seconds()

df.dropna(subset=['untracked_time'], inplace=True)

average_untracked_time = df['untracked_time'].mean()
total_untracked_time = df['untracked_time'].sum()

print(f'Average untracked time: {average_untracked_time} seconds')
print(f'Total untracked time: {total_untracked_time} seconds')