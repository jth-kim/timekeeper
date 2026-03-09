"""Investigation: This script investigates the factors contributing to the variability in untracked time between sessions and assesses their impact on overall time allocation against target priorities by analyzing the average untracked time for each client and project.
Generated: 20260304_235927 UTC
"""

import pandas as pd
from supabase_helper import query_entries

df = query_entries(days=30)

df['start'] = pd.to_datetime(df['start'])

df.sort_values(by='start', inplace=True)

df['untracked_time'] = (df['start'].diff().dt.total_seconds() / 3600)

df['untracked_time'] = df['untracked_time'].fillna(0)

print(df[['client_name', 'project_name', 'untracked_time']].groupby(['client_name', 'project_name'])['untracked_time'].mean())