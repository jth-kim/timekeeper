"""Investigation: This script investigates the factors contributing to the variability in untracked time between sessions across different clients, aiming to understand how these factors impact overall time allocation against target priorities. By analyzing recent time-tracking data and calculating mean untracked times for each client, it provides insights into potential imbalances or patterns that could inform adjustments to alert thresholds configuration.
Generated: 20260305_215626 UTC
"""


import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds

# Query recent entries (e.g., last 14 days)
entries = query_entries(days=14)

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate untracked time between sessions
df['untracked_time'] = df['start'].diff().dt.total_seconds()

# Group by client and calculate mean untracked time
mean_untracked_times = df.groupby('client_name')['untracked_time'].mean()

# Print results
print(mean_untracked_times)
