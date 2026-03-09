"""Investigation: This script investigates the task-level activity patterns within SEIFUKU that contribute to its variable session lengths across different days of the week. By analyzing recent time-tracking data and calculating mean session lengths for each day of the week, it provides insights into potential imbalances or patterns in time allocation.
Generated: 20260307_132446 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data for SEIFUKU
entries = query_entries(days=14, client='SEIFUKU')

# Convert to DataFrame and calculate session lengths
df = entries_to_dataframe(entries)
df['session_length'] = df['duration_seconds']

# Group by day of week and calculate mean session length
df['day_of_week'] = pd.to_datetime(df['start']).dt.dayofweek
mean_session_lengths = df.groupby('day_of_week')['session_length'].mean()

# Print results
print(mean_session_lengths)
