"""Investigation: This script investigates the specific task-level activities within SEIFUKU on Sundays and Thursdays that contribute to its longer session lengths, aiming to understand how these activities align with the Sovereign's broader objectives.
Generated: 20260307_045138 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data for SEIFUKU on Sundays and Thursdays
entries = query_entries(days=14)
seifuku_entries = [entry for entry in entries if entry['client_name'] == 'SEIFUKU']
sunday_thursday_entries = [entry for entry in seifuku_entries if (pd.to_datetime(entry['start']).dayofweek == 6) or (pd.to_datetime(entry['start']).dayofweek == 3)]

# Convert to DataFrame and calculate session lengths
df = entries_to_dataframe(sunday_thursday_entries)
session_lengths = df['duration_seconds']

# Group by task description and calculate mean session length for each task
task_session_lengths = df.groupby('description')['duration_seconds'].mean()

# Print top tasks contributing to longer sessions on Sundays and Thursdays
print(task_session_lengths.sort_values(ascending=False).head(10))
