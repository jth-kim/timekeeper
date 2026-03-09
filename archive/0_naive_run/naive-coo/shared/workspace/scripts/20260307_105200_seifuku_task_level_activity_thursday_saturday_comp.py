"""Investigation: This script compares task-level activity patterns within SEIFUKU on Thursdays vs. Saturdays to identify potential differences in session duration and alignment with the Sovereign's broader objectives.
Generated: 20260307_105200 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

df = entries_to_dataframe(query_entries(days=14))
seifuku_df = df[df['client_name'] == 'SEIFUKU']

thursday_seifuku = seifuku_df[seifuku_df['start'].dt.dayofweek == 3]
saturday_seifuku = seifuku_df[seifuku_df['start'].dt.dayofweek == 5]

print(thursday_seifuku.describe())
print(saturday_seifuku.describe())