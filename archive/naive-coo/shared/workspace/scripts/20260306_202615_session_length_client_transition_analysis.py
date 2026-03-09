"""Investigation: This script investigates the relationship between session lengths and client transitions over the last week, aiming to understand how time allocation varies across different clients and projects.
Generated: 20260306_202615 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query recent entries
entries = query_entries(days=7)

# Convert to DataFrame
df = entries_to_dataframe(entries)

# Calculate session length in seconds
df['session_length_seconds'] = df['duration_seconds']

# Group by client and calculate mean session length
client_session_lengths = df.groupby('client_name')['session_length_seconds'].mean()

# Print results
print(client_session_lengths)
