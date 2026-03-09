"""Investigation: This script investigates the patterns of client transitions between sessions, helping to understand how different clients are sequenced in the Sovereign's work schedule.
Generated: 20260304_234157 UTC
"""

import pandas as pd
from supabase_helper import query_entries

df = pd.DataFrame(query_entries(days=30))
# Ensure 'start' column is of correct data type for time-based analysis
df['start'] = pd.to_datetime(df['start'])

df_sorted = df.sort_values(by='start')
client_transitions = df_sorted[['client_name']].shift(-1)
df['next_client'] = client_transitions
transition_counts = df.groupby(['client_name', 'next_client']).size().reset_index(name='count')
print(transition_counts)