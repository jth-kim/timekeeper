"""Investigation: This script adjusts the dataframe to ensure the 'start' column is of the correct data type (datetime) for analysis and calculates untracked time between sessions, providing a foundation for assessing variability in untracked time.
Generated: 20260304_232712 UTC
"""

import pandas as pd
from supabase_helper import query_entries

df = pd.DataFrame(query_entries(days=30))
# Ensure 'start' column is of datetime type for analysis
df['start'] = pd.to_datetime(df['start'])

df['untracked_time'] = df['start'].diff().dt.total_seconds()
print(df.head())