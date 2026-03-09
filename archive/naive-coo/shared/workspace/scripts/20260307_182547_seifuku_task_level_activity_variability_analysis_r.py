"""Investigation: This script investigates the specific task-level activities within SEIFUKU that contribute to its variable session lengths across different days of the week. By analyzing recent time-tracking data and calculating mean session lengths for each day, it provides insights into potential imbalances or patterns in time allocation.
Generated: 20260307_182547 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data for SEIFUKU sessions
entries = query_entries(days=14, client='SEIFUKU')

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate session length in seconds
df['session_length'] = df['duration_seconds']

# Group by day of week and calculate mean session length
grouped_df = df.groupby('start_dt.dt.dayofweek')['session_length'].mean()

# Print results
print(grouped_df)
