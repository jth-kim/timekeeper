"""Investigation: This script investigates the factors contributing to the variability in untracked time between sessions across different clients, providing insights into potential imbalances or patterns that could inform adjustments to alert thresholds configuration.
Generated: 20260305_225433 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data
entries = query_entries(days=14)

# Convert to DataFrame
df = entries_to_dataframe(entries)

# Calculate untracked time between sessions
df['untracked_time'] = df['start'].diff().dt.total_seconds()

# Group by client and calculate mean untracked time
mean_untracked_time = df.groupby('client_name')['untracked_time'].mean()

# Print results
print(mean_untracked_time)
