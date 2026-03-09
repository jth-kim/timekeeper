"""Investigation: This script investigates the task-level activity patterns within SEIFUKU that contribute to its variable session lengths across different days of the week. By analyzing recent time-tracking data and calculating mean session lengths for each day of the week, it provides insights into how these activities align with the Sovereign's priorities and goals.
Generated: 20260307_152922 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data for SEIFUKU
entries = query_entries(days=14)
seifuku_entries = [entry for entry in entries if entry['client_name'] == 'SEIFUKU']

# Convert to DataFrame and calculate session lengths
df = entries_to_dataframe(seifuku_entries)
df['session_length'] = df['duration_seconds'] / 3600  # Convert seconds to hours

# Group by day of week and calculate mean session length
df['day_of_week'] = pd.to_datetime(df['start']).dt.dayofweek
mean_session_lengths = df.groupby('day_of_week')['session_length'].mean()

# Print results
print(mean_session_lengths)
