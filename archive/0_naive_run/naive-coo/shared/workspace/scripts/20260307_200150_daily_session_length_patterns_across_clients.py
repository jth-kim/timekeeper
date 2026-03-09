"""Investigation: This script investigates the daily patterns of session lengths for each client over the last 14 days, providing insights into how productivity varies across different days and clients.
Generated: 20260307_200150 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

days = 14
entries = query_entries(days=days)
df = entries_to_dataframe(entries)

daily_session_lengths = df.groupby([pd.Grouper(key='start', freq='D'), 'client_name'])['duration_seconds'].mean().reset_index()
print(daily_session_lengths)