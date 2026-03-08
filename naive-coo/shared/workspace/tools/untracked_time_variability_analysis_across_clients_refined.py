"""Investigation: This script investigates the factors contributing to the variability in untracked time between sessions across different clients and assesses their impact on overall time allocation against target priorities. It calculates the mean untracked time for each client, providing insights into potential imbalances or patterns that could inform adjustments to alert thresholds configuration.
Generated: 20260306_161420 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent entries to analyze untracked time variability
entries = query_entries(days=14)

# Convert entries to a DataFrame for easier analysis
df = entries_to_dataframe(entries)

# Calculate untracked time between sessions
df['untracked_time'] = df['start'].diff().dt.total_seconds()

# Group by client and calculate mean untracked time
mean_untracked_time_by_client = df.groupby('client_name')['untracked_time'].mean()

# Print the results
print(mean_untracked_time_by_client)
