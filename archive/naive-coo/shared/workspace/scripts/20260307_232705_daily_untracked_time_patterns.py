"""Investigation: This script investigates the daily patterns of gaps between sessions (untracked time) for each client over the last 14 days, providing insights into how these patterns impact overall time allocation against target priorities.
Generated: 20260307_232705 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

days = 14
entries = query_entries(days=days)
df = entries_to_dataframe(entries)

gaps_df = df[['start', 'stop']]
gaps_df['gap'] = gaps_df['start'].diff().dt.total_seconds()
gaps_df = gaps_df[1:]

gaps_by_client = gaps_df.groupby('client_name')['gap'].mean().reset_index()
print(gaps_by_client)