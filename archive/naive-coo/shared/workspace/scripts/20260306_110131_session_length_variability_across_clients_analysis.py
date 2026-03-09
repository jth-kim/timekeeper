"""Investigation: This script investigates the factors contributing to the variability in session lengths across different clients and assesses their impact on overall time allocation against target priorities. It queries recent time-tracking data, converts it into a pandas DataFrame, groups the data by client name and project name, calculates the mean duration for each group, and prints the results.
Generated: 20260306_110131 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

days = 30
entries = query_entries(days=days)
df = entries_to_dataframe(entries)

df['client_name'] = df['client_name'].astype('category')
df['project_name'] = df['project_name'].astype('category')

grouped_df = df.groupby(['client_name', 'project_name'])['duration_seconds'].mean().reset_index()
print(grouped_df)