"""Investigation: This script investigates the relationship between client transitions and session lengths by analyzing recent time-tracking data, calculating mean session lengths for each client and project, and examining patterns of client transitions to understand their impact on overall time allocation.
Generated: 20260306_173428 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data
entries = query_entries(days=14)

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Ensure 'start' and 'stop' columns are datetime
df['start'] = pd.to_datetime(df['start'])
df['stop'] = pd.to_datetime(df['stop'])

# Calculate session length in seconds
df['session_length_seconds'] = (df['stop'] - df['start']).dt.total_seconds()

# Group by client name and project name, then calculate mean session length for each group
grouped_df = df.groupby(['client_name', 'project_name'])['session_length_seconds'].mean().reset_index()

# Print the result
print(grouped_df)
