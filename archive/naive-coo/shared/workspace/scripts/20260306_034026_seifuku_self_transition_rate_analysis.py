"""Investigation: This script investigates the factors contributing to the high self-transition rate of SEIFUKU and assesses their impact on overall time allocation against target priorities. It calculates the self-transition rates for each tag within SEIFUKU and prints the results.
Generated: 20260306_034026 UTC
"""

import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds, entries_to_dataframe

df = entries_to_dataframe(query_entries(days=30))
seifuku_df = df[df['client_name'] == 'SEIFUKU']
self_transition_rates = seifuku_df['tags'].value_counts(normalize=True)
print(self_transition_rates)