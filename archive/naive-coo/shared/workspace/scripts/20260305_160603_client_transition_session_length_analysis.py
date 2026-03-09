"""Investigation: This script investigates the relationship between session lengths and client transitions, aiming to understand how time allocation varies across different clients and projects. It calculates the mean session length for each client over the last 14 days and prints these averages in a clear format.
Generated: 20260305_160603 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

df = entries_to_dataframe(query_entries(days=14))
print(df.head())
print(df['client_name'].value_counts())
print(df.groupby('client_name')['duration_seconds'].mean())