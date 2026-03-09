"""Investigation: This script investigates the patterns of client transitions between sessions to understand how different clients are sequenced in the Sovereign's work schedule and assesses their impact on overall time allocation.
Generated: 20260305_032220 UTC
"""

import pandas as pd
from supabase_helper import query_entries

df = pd.DataFrame(query_entries(days=30))
print(df.head())
# Calculate transition frequencies
counts = df['client_name'].value_counts()
transitions = df[['client_name', 'project_name']].shift().add_suffix('_prev')
df = pd.concat([df, transitions], axis=1)
transition_freq = df.groupby(['client_name', 'client_name_prev']).size().reset_index(name='freq')
print(transition_freq)