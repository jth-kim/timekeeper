"""Investigation: This script investigates the factors contributing to the variability in session lengths across different days of the week for each client, aiming to understand how productivity varies across different days and clients.
Generated: 20260307_032953 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data
entries = query_entries(days=14)

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate session length in seconds
df['session_length_seconds'] = df['duration_seconds']

# Group by client and day of week
grouped_df = df.groupby(['client_name', pd.Grouper(key='start', freq='D')])

# Calculate mean session length for each group
mean_session_lengths = grouped_df['session_length_seconds'].mean()

# Print the results
print(mean_session_lengths)
