"""Investigation: This script investigates the gaps between sessions (untracked time) for each client over the last week and calculates the mean gap length for each client, providing insights into how these gaps impact overall time allocation.
Generated: 20260306_132247 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

df = entries_to_dataframe(query_entries(days=7))

df['start'] = pd.to_datetime(df['start'])

df['stop'] = pd.to_datetime(df['stop'])

df['session_length'] = (df['stop'] - df['start']).dt.total_seconds()

df.sort_values(by='start', inplace=True)

gaps_df = pd.DataFrame({'gap_start': df['start'].shift(1), 'gap_end': df['start'], 'client_name': df['client_name']})

gaps_df.dropna(inplace=True)

gaps_df['gap_length'] = (gaps_df['gap_end'] - gaps_df['gap_start']).dt.total_seconds()

print(gaps_df.groupby('client_name')['gap_length'].mean())