"""Investigation: This script investigates the task-level activity patterns within SEIFUKU that contribute to its variable session lengths across different days of the week. By analyzing recent time-tracking data and calculating mean session lengths for each day of the week, it provides insights into potential imbalances or patterns in time allocation.
Generated: 20260307_122005 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data for SEIFUKU
entries = query_entries(days=14)
seifuku_entries = [entry for entry in entries if entry['client_name'] == 'SEIFUKU']

# Convert entries to a pandas DataFrame with proper types
df = entries_to_dataframe(seifuku_entries)

# Group by day of the week and calculate mean session length
day_of_week_session_lengths = df.groupby(df['start'].dt.dayofweek)['duration_seconds'].mean()

# Print the results
print(day_of_week_session_lengths)
