"""Investigation: This script refines the analysis of average session duration in SEIFUKU by correctly handling data processing and providing a reliable insight into time allocation patterns.
Generated: 20260306_114027 UTC
"""

import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds, entries_to_dataframe

df = entries_to_dataframe(query_entries(days=14))
seifuku_df = df[df['client_name'] == 'SEIFUKU']
seifuku_session_durations = seifuku_df['duration_seconds']
print(seifuku_session_durations.mean())