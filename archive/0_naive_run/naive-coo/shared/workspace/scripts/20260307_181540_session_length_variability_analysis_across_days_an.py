"""Investigation: This script investigates the primary factors contributing to session length variability across different days of the week for each client, providing insights into how these patterns impact overall time allocation against target priorities. It calculates mean session lengths for each client by day of the week and prints the results in a clear format.
Generated: 20260307_181540 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent entries
entries = query_entries(days=14)

# Convert to DataFrame
df = entries_to_dataframe(entries)

# Calculate session length in seconds
df['session_length'] = df['duration_seconds']

# Group by client and day of week
grouped_df = df.groupby(['client_name', 'start_dt.dt.dayofweek'])

# Calculate mean session length for each group
mean_session_lengths = grouped_df['session_length'].mean()

# Print results
print(mean_session_lengths)
