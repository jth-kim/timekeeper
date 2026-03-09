"""Investigation: This script investigates the underlying causes of the discrepancies in session lengths across clients, particularly for STAR on Thursdays. It calculates the average session length for each client and day of the week, identifies discrepancies in session lengths for STAR on Thursdays, and prints the results.
Generated: 20260305_214404 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

df = entries_to_dataframe(query_entries(days=14))
print(df.head())
# Calculate session lengths for each client and day of the week
session_lengths = df.groupby(['client_name', 'start.dt.dayofweek'])['duration_seconds'].mean()
print(session_lengths)
# Identify discrepancies in session lengths for STAR on Thursdays
star_thursday_sessions = df[(df['client_name'] == 'STAR') & (df['start'].dt.dayofweek == 3)]
print(star_thursday_sessions)