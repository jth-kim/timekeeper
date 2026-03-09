"""Investigation: This script investigates task-level activities within each client that contribute to session length variability. It calculates the mean session length for each task within each client and prints the results, providing insights into how these activities impact overall productivity and goal achievement.
Generated: 20260306_185041 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data for the last two weeks
entries = query_entries(days=14)

# Convert the entries into a DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate session lengths in seconds
df['session_length_seconds'] = df['duration_seconds']

# Group by client and project, then calculate mean session length
mean_session_lengths = df.groupby(['client_name', 'project_name'])['session_length_seconds'].mean().reset_index()

# Print the results
print(mean_session_lengths)
