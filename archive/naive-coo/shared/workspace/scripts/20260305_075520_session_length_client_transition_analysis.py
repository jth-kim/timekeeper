"""Investigation: This script investigates the relationship between session lengths and client transitions to understand how time allocation varies across different clients and projects.
Generated: 20260305_075520 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query recent entries
entries = query_entries(days=14)

# Convert to DataFrame
df = pd.DataFrame(entries)

# Ensure 'start' and 'stop' are datetime
df['start'] = pd.to_datetime(df['start'])
df['stop'] = pd.to_datetime(df['stop'])

# Calculate session length in seconds
df['session_length'] = (df['stop'] - df['start']).dt.total_seconds()

# Group by client and calculate mean session length
mean_session_lengths = df.groupby('client_name')['session_length'].mean()

# Print results
print(mean_session_lengths)
