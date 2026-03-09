"""Investigation: This script investigates the relationship between session length and client transitions over the last 30 days, aiming to understand how time allocation varies across different clients and projects.
Generated: 20260305_120009 UTC
"""


from supabase_helper import query_entries, entries_to_dataframe
import pandas as pd

# Query recent entries (last 30 days)
entries = query_entries(days=30)

# Convert to dataframe with proper types
df = entries_to_dataframe(entries)

# Calculate session length in seconds
df['session_length_seconds'] = df['duration_seconds']

# Group by client and calculate mean session length
client_mean_session_lengths = df.groupby('client_name')['session_length_seconds'].mean()

# Print the results
print(client_mean_session_lengths)
