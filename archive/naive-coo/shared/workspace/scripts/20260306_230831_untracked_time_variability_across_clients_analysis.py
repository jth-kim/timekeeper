"""Investigation: This script investigates the factors contributing to the variability in untracked time between sessions across different clients and assesses their impact on overall time allocation against target priorities.
Generated: 20260306_230831 UTC
"""


import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds

# Query recent entries (last 30 days)
entries = query_entries(days=30)

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate untracked time between sessions for each client
df['untracked_time'] = df.apply(lambda row: row['start'] - row['stop'], axis=1)

# Group by client and calculate mean untracked time
client_untracked_times = df.groupby('client_name')['untracked_time'].mean()

# Print results
print(client_untracked_times)
