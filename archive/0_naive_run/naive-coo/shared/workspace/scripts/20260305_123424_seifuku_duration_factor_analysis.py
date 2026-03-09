"""Investigation: This script investigates the factors contributing to SEIFUKU's high duration by analyzing recent entries, calculating session lengths, and grouping by day of week to identify patterns in time allocation.
Generated: 20260305_123424 UTC
"""


import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds

# Query recent entries for SEIFUKU
entries = query_entries(days=14, client='SEIFUKU')

# Convert to DataFrame with proper duration handling
df = entries_to_dataframe(entries)

# Calculate session lengths and group by day of week
df['session_length'] = df['duration_seconds']
df['day_of_week'] = pd.to_datetime(df['start']).dt.dayofweek

# Group by day of week and calculate mean session length
mean_session_lengths = df.groupby('day_of_week')['session_length'].mean()

# Print results
print(mean_session_lengths)
