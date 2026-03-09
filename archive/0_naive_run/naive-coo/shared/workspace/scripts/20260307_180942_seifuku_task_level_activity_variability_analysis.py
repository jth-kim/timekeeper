"""Investigation: This script investigates the specific task-level activities within SEIFUKU that contribute to its variable session lengths across different days of the week. By analyzing recent time-tracking data and calculating mean session lengths for each project within SEIFUKU by day of the week, it provides insights into potential imbalances or patterns in time allocation.
Generated: 20260307_180942 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data for SEIFUKU sessions
seifuku_entries = [entry for entry in query_entries(days=14) if entry['client_name'] == 'SEIFUKU']

# Convert to DataFrame with proper types
df = entries_to_dataframe(seifuku_entries)

# Calculate session lengths and group by day of the week
df['session_length'] = df['duration_seconds']
df['day_of_week'] = pd.to_datetime(df['start']).dt.dayofweek

grouped_df = df.groupby(['client_name', 'project_name', 'day_of_week'])['session_length'].mean().reset_index()

# Print results to identify patterns or anomalies
print(grouped_df)
