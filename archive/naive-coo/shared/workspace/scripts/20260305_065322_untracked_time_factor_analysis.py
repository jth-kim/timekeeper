"""Investigation: This script investigates the factors contributing to the significant variability in untracked time across clients. By analyzing recent time-tracking data, it calculates the mean untracked time for each client and provides insights into potential imbalances or patterns that could inform adjustments to achieve a more balanced time allocation.
Generated: 20260305_065322 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query recent entries (last 30 days)
entries = query_entries(days=30)

# Convert to DataFrame for easier manipulation
df = pd.DataFrame(entries)

# Calculate untracked time between sessions
df['untracked_time'] = df['start'].diff().dt.total_seconds()

# Group by client and calculate mean untracked time
mean_untracked_times = df.groupby('client_name')['untracked_time'].mean()

# Print results
print(mean_untracked_times)
