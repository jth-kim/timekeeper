"""Investigation: This script investigates the relationship between session lengths and client transitions over the last week, aiming to understand how time allocation varies across different clients and projects. It calculates mean session lengths for each client and examines the patterns of client transitions to understand their impact on overall time allocation against target priorities.
Generated: 20260305_222629 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent entries (last week)
entries = query_entries(days=7)

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate session length in seconds
df['session_length_seconds'] = df['duration_seconds']

# Group by client and project, calculate mean session length
mean_session_lengths = df.groupby(['client_name', 'project_name'])['session_length_seconds'].mean().reset_index()

# Print results
print(mean_session_lengths)
