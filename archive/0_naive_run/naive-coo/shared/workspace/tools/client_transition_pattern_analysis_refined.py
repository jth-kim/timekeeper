"""Investigation: This script investigates the patterns of client transitions between sessions over the last week and their impact on overall time allocation. By analyzing recent time-tracking data, calculating mean session lengths for each client transition, and printing the results in a clear format, it provides insights into how different clients are sequenced in the Sovereign's work schedule.
Generated: 20260307_134507 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query recent entries
entries = query_entries(days=7)

# Convert to DataFrame
df = pd.DataFrame(entries)

# Ensure 'start' and 'stop' columns are datetime
df['start'] = pd.to_datetime(df['start'])
df['stop'] = pd.to_datetime(df['stop'])

# Calculate session length in seconds
df['session_length_seconds'] = (df['stop'] - df['start']).dt.total_seconds()

# Group by client name and project name, then calculate mean session length
client_transition_patterns = df.groupby(['client_name', 'project_name'])['session_length_seconds'].mean().reset_index()

# Print the results
print(client_transition_patterns)
