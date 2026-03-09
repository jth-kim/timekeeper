"""Investigation: This script investigates task-level activity patterns within SEIFUKU that contribute to its variable session lengths across different days of the week. By analyzing recent time-tracking data, calculating mean session lengths for each day of the week, and grouping tasks by duration, it provides insights into potential imbalances or patterns in time allocation.
Generated: 20260307_130156 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data for SEIFUKU
entries = query_entries(days=14, client='SEIFUKU')

# Convert entries to a pandas DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate session lengths in seconds
df['session_length'] = df['duration_seconds']

# Group by day of week and calculate mean session length for each group
day_of_week_session_lengths = df.groupby(df['start'].dt.dayofweek)['session_length'].mean()

# Print the results
print(day_of_week_session_lengths)
