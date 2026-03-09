"""Investigation: This script investigates the relationship between client transitions and session lengths, aiming to understand how time allocation varies across different clients and projects. It calculates the mean session length for each client over the last 14 days and prints these averages in a clear format.
Generated: 20260305_154258 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent entries
entries = query_entries(days=14)

# Convert to DataFrame
df = entries_to_dataframe(entries)

# Calculate session length in seconds
df['session_length_seconds'] = df['duration_seconds']

# Group by client and calculate mean session length
client_mean_session_lengths = df.groupby('client_name')['session_length_seconds'].mean()

# Print results
print(client_mean_session_lengths)
