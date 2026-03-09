"""Investigation: This script investigates the relationship between session lengths and client transitions over the last week, aiming to understand how time allocation varies across different clients and projects. It calculates mean session lengths for each client and examines patterns of client transitions to inform adjustments to priorities or alert thresholds.
Generated: 20260306_194211 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

df = entries_to_dataframe(query_entries(days=7))
# Ensure 'start' and 'stop' are datetime format for calculations
df['start'] = pd.to_datetime(df['start'])
df['stop'] = pd.to_datetime(df['stop'])

df['session_length_seconds'] = (df['stop'] - df['start']).dt.total_seconds()

df_grouped = df.groupby(['client_name', 'project_name'])['session_length_seconds'].mean().reset_index()
print(df_grouped)
