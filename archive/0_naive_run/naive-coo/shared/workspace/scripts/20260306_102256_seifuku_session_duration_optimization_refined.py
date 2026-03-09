"""Investigation: This script investigates the factors contributing to the high average session duration in SEIFUKU and how they can be optimized to improve overall time allocation efficiency. It queries the last 30 days of entries, filters for SEIFUKU entries, and calculates the mean duration in seconds.
Generated: 20260306_102256 UTC
"""

import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds, entries_to_dataframe

df = entries_to_dataframe(query_entries(days=30))
seifuku_df = df[df['client_name'] == 'SEIFUKU']
print(seifuku_df.head())
print(seifuku_df['duration_seconds'].mean())