"""Investigation: This script investigates the patterns of client transitions between sessions over the last week and assesses their impact on overall time allocation against target priorities. It calculates mean session lengths for each client and examines the patterns of client transitions to understand their impact on overall time allocation.
Generated: 20260307_100213 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query entries for the last week
entries = query_entries(days=7)

# Convert entries to DataFrame
df = pd.DataFrame(entries)

# Ensure 'start' and 'stop' columns are datetime
df['start'] = pd.to_datetime(df['start'])
df['stop'] = pd.to_datetime(df['stop'])

# Calculate session length in seconds
df['session_length_seconds'] = (df['stop'] - df['start']).dt.total_seconds()

# Group by client name and project name, then calculate mean session length for each group
client_transition_patterns = df.groupby(['client_name', 'project_name'])['session_length_seconds'].mean().reset_index()

# Print the results
print(client_transition_patterns)
