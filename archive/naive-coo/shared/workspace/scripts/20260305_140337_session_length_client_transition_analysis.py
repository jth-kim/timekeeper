"""Investigation: This script investigates the relationship between session lengths and client transitions, aiming to understand how time allocation varies across different clients and projects. It calculates the average session length for each client over the last 14 days and prints these averages in a clear format.
Generated: 20260305_140337 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent entries
entries = query_entries(days=14)

# Convert to DataFrame
df = entries_to_dataframe(entries)

# Calculate session lengths
df['session_length'] = df['duration_seconds'] / 3600  # Convert seconds to hours

# Group by client and calculate mean session length
client_session_lengths = df.groupby('client_name')['session_length'].mean()

# Print results
print(client_session_lengths)
