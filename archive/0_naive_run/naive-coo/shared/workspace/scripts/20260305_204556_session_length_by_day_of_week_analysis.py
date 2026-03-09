"""Investigation: This script investigates the session length patterns by day of the week for each client over the last 14 days, providing insights into how productivity varies across different days and clients.
Generated: 20260305_204556 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

df = entries_to_dataframe(query_entries(days=14))
# Calculate session length in seconds and convert to minutes for easier interpretation
df['session_length_minutes'] = df['duration_seconds'] / 60

grouped_df = df.groupby([pd.Grouper(key='start', freq='D'), 'client_name'])['session_length_minutes'].mean().reset_index()
print(grouped_df)