"""Investigation: This script investigates the factors contributing to SEIFUKU's high duration by analyzing recent entries, calculating session lengths, and grouping by day of week to identify patterns in time allocation.
Generated: 20260305_124029 UTC
"""


import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds

# Query recent entries for SEIFUKU
entries = query_entries(days=14, client='SEIFUKU')

# Convert entries to a DataFrame with proper types
df = pd.DataFrame(entries)

# Calculate session lengths in seconds
df['duration_seconds'] = df['duration'].apply(parse_duration_seconds)

# Group by day of week and calculate mean session length
mean_session_lengths = df.groupby(df['start'].dt.dayofweek)['duration_seconds'].mean()

# Print the results
print(mean_session_lengths)
