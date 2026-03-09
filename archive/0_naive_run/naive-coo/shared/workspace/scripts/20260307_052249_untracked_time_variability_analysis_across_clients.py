"""Investigation: This script investigates the factors contributing to the variability in untracked time between sessions across different clients and assesses their impact on overall time allocation against target priorities. It calculates the mean untracked time for each client, providing insights into potential imbalances or patterns that could inform adjustments to alert thresholds configuration.
Generated: 20260307_052249 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query recent entries for analysis
entries = query_entries(days=14)

# Convert entries to a DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate untracked time between sessions
df['untracked_time'] = df['start'].diff().dt.total_seconds()

# Group by client and calculate mean untracked time
mean_untracked_time = df.groupby('client_name')['untracked_time'].mean()

# Print results
print(mean_untracked_time)
