"""Investigation: This script investigates the gaps between sessions (untracked time) for each client over the last 14 days, calculating the mean gap length for each client and providing insights into how these gaps impact overall time allocation. It addresses a new angle by focusing on untracked time, which has been mentioned in previous investigations but not thoroughly explored.
Generated: 20260307_184227 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent entries
entries = query_entries(days=14)

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate untracked time between sessions
df['untracked_time'] = df['start'].diff().apply(lambda x: x.total_seconds() if x else 0)

# Group by client and calculate mean untracked time
mean_untracked_time = df.groupby('client_name')['untracked_time'].mean()

# Print results
print(mean_untracked_time)
