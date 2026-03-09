"""Investigation: This script analyzes the session length variability across tasks within each client over the last 14 days, providing insights into potential imbalances in time allocation and factors contributing to these imbalances.
Generated: 20260306_012120 UTC
"""

import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds, entries_to_dataframe

tasks = query_entries(days=14)
df = entries_to_dataframe(tasks)

df['duration_hours'] = df['duration_seconds'] / 3600

df_grouped = df.groupby(['client_name', 'project_name'])['duration_hours'].mean().reset_index()

df_grouped = df_grouped.sort_values(by='duration_hours', ascending=False)
print(df_grouped)