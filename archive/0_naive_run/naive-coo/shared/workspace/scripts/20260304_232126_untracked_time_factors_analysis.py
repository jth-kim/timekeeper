"""Investigation: This script investigates the specific activities or factors that contribute to the significant variability in untracked time between sessions and assesses their impact on overall time allocation against target priorities.
Generated: 20260304_232126 UTC
"""

import pandas as pd
from supabase_helper import query_entries, read_memory

df = pd.DataFrame(query_entries(days=7))
print(df.head())
# Calculate untracked time between sessions
df['untracked_time'] = df['start'].diff().dt.total_seconds() / 3600
print(df['untracked_time'].describe())
# Identify factors contributing to variability in untracked time
factors_df = df[['client_name', 'project_name', 'tags', 'description', 'untracked_time']]
print(factors_df.head())