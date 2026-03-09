"""Investigation: This script investigates the underlying reasons for SEIFUKU's longer sessions on Sundays and Thursdays, providing insights into potential patterns in time allocation that could impact long-term goals.
Generated: 20260305_122059 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent entries for SEIFUKU
entries = query_entries(days=14, client='SEIFUKU')

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate session lengths
session_lengths = df['duration_seconds']

# Group by day of week and calculate mean session length
mean_session_lengths = session_lengths.groupby(df['start'].dt.dayofweek).mean()

# Print results
print(mean_session_lengths)
