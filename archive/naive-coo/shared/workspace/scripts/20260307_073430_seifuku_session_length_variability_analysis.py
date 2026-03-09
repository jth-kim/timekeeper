"""Investigation: This script analyzes the variability in session lengths for SEIFUKU across different days of the week, aiming to understand how these patterns align with the Sovereign's broader objectives.
Generated: 20260307_073430 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query recent entries for SEIFUKU
entries = query_entries(days=14, client_name='SEIFUKU')

# Convert to DataFrame and calculate session lengths
df = entries_to_dataframe(entries)
session_lengths = df['duration_seconds']

# Group by day of week and calculate mean session length
mean_session_lengths = session_lengths.groupby(df['start'].dt.dayofweek).mean()

# Print results
print(mean_session_lengths)