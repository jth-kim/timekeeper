"""Investigation: This script investigates the factors contributing to the variability in untracked time between sessions and assesses their impact on overall time allocation against target priorities. It calculates the untracked time between each session, groups the data by client, and prints summary statistics for the untracked time.
Generated: 20260305_121044 UTC
"""

import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds, entries_to_dataframe

df = entries_to_dataframe(query_entries(days=30))

df['start'] = pd.to_datetime(df['start'])

df['end'] = df['start'] + pd.to_timedelta(df['duration_seconds'], unit='s')

df.sort_values(by='start', inplace=True)

df['untracked_time'] = (df['start'] - df['end'].shift(1)).dt.total_seconds()

df['untracked_time'] = df['untracked_time'].fillna(0)

print(df[['client_name', 'untracked_time']].groupby('client_name')['untracked_time'].describe())