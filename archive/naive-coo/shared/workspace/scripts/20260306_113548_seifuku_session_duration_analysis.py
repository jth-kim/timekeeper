"""Investigation: This script investigates the factors contributing to the high average session duration in SEIFUKU by analyzing recent time-tracking data and calculating mean session lengths for each task within SEIFUKU. The goal is to understand how these factors impact overall time allocation against target priorities.
Generated: 20260306_113548 UTC
"""

import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds, entries_to_dataframe

df = entries_to_dataframe(query_entries(days=30))
seifuku_df = df[df['client_name'] == 'SEIFUKU']
seifuku_avg_session_length = seifuku_df['duration_seconds'].mean()
print(f'SEIFUKU average session length: {seifuku_avg_session_length} seconds')