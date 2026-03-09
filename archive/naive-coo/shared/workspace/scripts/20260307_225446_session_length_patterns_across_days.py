"""Investigation: This script investigates the patterns of session lengths across different days of the week for each client, providing insights into how productivity varies across different days and clients. By analyzing recent time-tracking data and calculating mean session lengths for each client by day of the week, it aims to understand how these patterns impact overall time allocation against target priorities.
Generated: 20260307_225446 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data
entries = query_entries(days=14)

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate session lengths
df['session_length'] = df['duration_seconds']

# Group by client and day of week
grouped_df = df.groupby(['client_name', pd.Grouper(key='start', freq='D')])

# Calculate mean session length for each group
mean_session_lengths = grouped_df['session_length'].mean()

# Print results in a clear format
print(mean_session_lengths)
