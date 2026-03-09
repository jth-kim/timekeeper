"""Investigation: This script investigates the task-level activities within SEIFUKU that contribute to its variable session lengths across different days of the week, aiming to understand how these factors impact overall productivity.
Generated: 20260307_142357 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query recent entries for SEIFUKU
entries = query_entries(days=14, client='SEIFUKU')

# Convert to DataFrame and calculate session lengths
df = pd.DataFrame(entries)
df['duration_seconds'] = df['duration'].apply(lambda x: parse_duration_seconds(x))
df['session_length_hours'] = df['duration_seconds'] / 3600

# Group by day of week and calculate mean session length
df['start_date'] = pd.to_datetime(df['start']).dt.date
df['day_of_week'] = pd.to_datetime(df['start']).dt.dayofweek

mean_session_lengths = df.groupby('day_of_week')['session_length_hours'].mean()

print(mean_session_lengths)
