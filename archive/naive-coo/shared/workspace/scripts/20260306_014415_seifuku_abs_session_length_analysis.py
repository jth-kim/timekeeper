"""Investigation: This script investigates the factors contributing to the high average session duration for SEIFUKU's ABS task and assesses its impact on overall time allocation against target priorities. It calculates the mean session length for SEIFUKU's ABS task over the last 14 days and prints this value.
Generated: 20260306_014415 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

df = entries_to_dataframe(query_entries(days=14))
seifuku_abs_df = df[(df['client_name'] == 'SEIFUKU') & (df['project_name'] == 'ABS')]
abs_average_session_length = seifuku_abs_df['duration_seconds'].mean()
print(f'The average session length for SEIFUKU\'s ABS task is {abs_average_session_length} seconds.')
