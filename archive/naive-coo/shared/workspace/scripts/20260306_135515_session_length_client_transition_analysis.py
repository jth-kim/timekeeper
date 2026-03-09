"""Investigation: This script investigates the relationship between session lengths and client transitions over the last week, providing insights into how time allocation varies across different clients and projects. It calculates mean session lengths for each client and examines the patterns of client transitions to understand their impact on overall time allocation against target priorities.
Generated: 20260306_135515 UTC
"""


import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds

# Query recent entries
entries = query_entries(days=7)

# Convert to DataFrame with proper types
df = pd.DataFrame(entries)
df['start'] = pd.to_datetime(df['start'])
df['stop'] = pd.to_datetime(df['stop'])
df['duration_seconds'] = df['duration'].apply(parse_duration_seconds)

# Calculate session length in seconds
df['session_length_seconds'] = df['duration_seconds']

# Group by client and calculate mean session length
client_mean_session_lengths = df.groupby('client_name')['session_length_seconds'].mean()

# Print results
print(client_mean_session_lengths)
