"""Investigation: This script investigates the gaps between sessions (untracked time) for each client over the last week and calculates the mean gap length for each client, providing insights into how these gaps impact overall time allocation.
Generated: 20260307_074610 UTC
"""

import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds

days = 7
clients = ['SEIFUKU', 'STAR', 'BBOY', 'BOJ']
entries = query_entries(days=days)
df = entries_to_dataframe(entries)
df['start'] = pd.to_datetime(df['start'])
df['stop'] = pd.to_datetime(df['stop'])
df['duration_seconds'] = df['duration_seconds'].astype(float)
gaps_df = pd.DataFrame(columns=['client', 'gap_length_seconds'])
for i in range(len(df) - 1):
    if df.iloc[i]['client_name'] == df.iloc[i+1]['client_name']:
        gap_length_seconds = (df.iloc[i+1]['start'] - df.iloc[i]['stop']).total_seconds()
        gaps_df = pd.concat([gaps_df, pd.DataFrame({'client': [df.iloc[i]['client_name']], 'gap_length_seconds': [gap_length_seconds]})], ignore_index=True)
gaps_df_grouped = gaps_df.groupby('client')['gap_length_seconds'].mean().reset_index()
print(gaps_df_grouped)