"""Investigation: This script investigates task-level activities within SEIFUKU on Saturdays and Thursdays that contribute to its longer session lengths, aiming to understand how these activities align with the Sovereign's broader objectives.
Generated: 20260307_070341 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data for SEIFUKU on Saturdays and Thursdays
seifuku_entries = query_entries(days=14, client_name='SEIFUKU')

# Convert the data into a DataFrame with proper types
df_seifuku = entries_to_dataframe(seifuku_entries)

# Calculate session lengths in seconds
df_seifuku['session_length_seconds'] = df_seifuku['duration_seconds']

# Filter for Saturdays and Thursdays
saturday_thursday_df = df_seifuku[(df_seifuku['start'].dt.dayofweek == 5) | (df_seifuku['start'].dt.dayofweek == 3)]

# Group by project name and calculate mean session length
project_session_lengths = saturday_thursday_df.groupby('project_name')['session_length_seconds'].mean().reset_index()

# Print the results in a sorted format to identify projects with longer sessions
print(project_session_lengths.sort_values(by='session_length_seconds', ascending=False))
