"""Investigation: This script investigates the session length patterns by time of day for each client over the last week, providing insights into how productivity varies across different times of the day and clients.
Generated: 20260305_093307 UTC
"""

import pandas as pd
from supabase_helper import query_entries

df = pd.DataFrame(query_entries(days=7))

df['start'] = pd.to_datetime(df['start'])
df['hour'] = df['start'].dt.hour

groups = df.groupby(['client_name', 'hour'])
print(groups['duration'].mean())