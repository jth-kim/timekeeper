"""Investigation: This script analyzes the patterns of client transitions between sessions over the last week, providing insights into how these transitions impact overall time allocation. It calculates the number of times each client transition occurs and the mean session length following each transition, offering a detailed view of how the Sovereign's work schedule varies across different clients.
Generated: 20260307_201230 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

df = entries_to_dataframe(query_entries(days=7))
# Ensure 'start' and 'stop' columns are datetime format for easier manipulation
df['start'] = pd.to_datetime(df['start'])
df['stop'] = pd.to_datetime(df['stop'])

df_sorted = df.sort_values(by='start')  # Sort entries by start time to analyze transitions

current_client = None
transition_counts = {}
for index, row in df_sorted.iterrows():
    if current_client is not None and row['client_name'] != current_client:
        transition_key = f'{current_client} -> {row[