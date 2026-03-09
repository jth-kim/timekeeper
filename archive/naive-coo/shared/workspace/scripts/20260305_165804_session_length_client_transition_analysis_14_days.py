"""Investigation: This script investigates the relationship between session lengths and client transitions over the last 14 days, providing insights into how time allocation varies across different clients and projects.
Generated: 20260305_165804 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

df = entries_to_dataframe(query_entries(days=14))
print(df.groupby('client_name')['duration_seconds'].mean())
print(df['client_name'].value_counts())
print(df.groupby('client_name')['project_name'].value_counts())