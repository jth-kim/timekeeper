"""Investigation: This script investigates the task-level activities within SEIFUKU that contribute to its variable session lengths across different days of the week. By analyzing recent time-tracking data and calculating mean session lengths for each day of the week, it provides insights into potential imbalances or patterns in time allocation.
Generated: 20260307_144328 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data for SEIFUKU
entries = query_entries(days=14, client='SEIFUKU')

# Convert entries to a pandas DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate session lengths in seconds
df['session_length_seconds'] = df['duration_seconds']

# Group by day of the week and calculate mean session length
mean_session_lengths = df.groupby(df['start'].dt.dayofweek)['session_length_seconds'].mean()

# Print the results
print(mean_session_lengths)
