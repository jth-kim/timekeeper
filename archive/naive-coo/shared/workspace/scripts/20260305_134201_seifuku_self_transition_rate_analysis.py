"""Investigation: This script investigates the factors contributing to SEIFUKU's high self-transition rate and assesses its impact on overall time allocation against target priorities.
Generated: 20260305_134201 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

df = entries_to_dataframe(query_entries(days=14))
# Filter for SEIFUKU entries and calculate self-transition rate
seifuku_df = df[df['client_name'] == 'SEIFUKU']
self_transition_rate = seifuku_df.shape[0] / len(df)
print(f'SEIFUKU self-transition rate: {self_transition_rate}')