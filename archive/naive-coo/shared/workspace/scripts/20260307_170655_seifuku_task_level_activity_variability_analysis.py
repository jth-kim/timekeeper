"""Investigation: This script investigates the task-level activity patterns within SEIFUKU that contribute to its variable session lengths across different days of the week. By analyzing recent time-tracking data and calculating mean session lengths for each project within SEIFUKU by day of the week, it provides insights into potential imbalances or patterns in time allocation.
Generated: 20260307_170655 UTC
"""


import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds

# Query recent entries for SEIFUKU
seifuku_entries = [entry for entry in query_entries(days=14) if entry['client_name'] == 'SEIFUKU']

# Convert to DataFrame and calculate session lengths
df = pd.DataFrame(seifuku_entries)
df['session_length'] = df['duration'].apply(parse_duration_seconds)

# Group by day of week and project, calculate mean session length
grouped_df = df.groupby(['start_dt.dt.dayofweek', 'project_name'])['session_length'].mean().reset_index()

# Print results
print(grouped_df)