"""Investigation: This script investigates the factors contributing to the variability in untracked time between sessions across different clients. It calculates the mean untracked time for each client and prints the results, providing insights into potential imbalances or patterns that could inform adjustments to priorities or alert thresholds.
Generated: 20260306_154854 UTC
"""


import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds

# Query recent entries (last 14 days)
entries = query_entries(days=14)

# Convert entries to DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate untracked time between sessions for each client
df['untracked_time'] = df['start'].diff().apply(lambda x: x.total_seconds() if x else 0)

# Group by client and calculate mean untracked time
mean_untracked_time_by_client = df.groupby('client_name')['untracked_time'].mean()

# Print results
print(mean_untracked_time_by_client)
