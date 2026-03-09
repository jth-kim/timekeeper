"""Investigation: This script calculates the average untracked time between sessions for each client over the last week, providing insight into potential patterns or issues with time allocation.
Generated: 20260305_080414 UTC
"""

import pandas as pd
from supabase_helper import query_entries

days = 7
entries = query_entries(days=days)

data = []
for i in range(len(entries) - 1):
    session_end = entries[i]['stop']
    next_session_start = entries[i+1]['start']
    untracked_time = (next_session_start - session_end).total_seconds()
    data.append({'client': entries[i+1]['client_name'], 'untracked_time': untracked_time})

df = pd.DataFrame(data)
grouped_df = df.groupby('client')['untracked_time'].mean().reset_index()
print(grouped_df)