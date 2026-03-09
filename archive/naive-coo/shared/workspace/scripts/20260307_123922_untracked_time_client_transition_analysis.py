"""Investigation: This script investigates the gaps between sessions (untracked time) for each client over the last week and calculates the mean gap length for each client, providing insights into how these gaps impact overall time allocation.
Generated: 20260307_123922 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query entries for the last week
entries = query_entries(days=7)

# Convert entries to a DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate untracked time between sessions
df['untracked_time'] = df['start'].diff().fillna(0)

# Group by client and calculate mean untracked time
mean_untracked_time = df.groupby('client_name')['untracked_time'].mean()

# Print the results
print(mean_untracked_time)
