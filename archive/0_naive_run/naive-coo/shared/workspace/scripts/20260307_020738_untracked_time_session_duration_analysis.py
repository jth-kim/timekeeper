"""Investigation: This script investigates the relationship between gaps in session start times (untracked time) and subsequent session durations across different clients, providing insights into potential patterns or correlations that could inform adjustments to priorities or alert thresholds.
Generated: 20260307_020738 UTC
"""


import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds

# Query recent entries
entries = query_entries(days=14)

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate untracked time between sessions
df['untracked_time'] = df['start'].diff().apply(lambda x: x.total_seconds() if x else 0)

# Group by client and calculate mean untracked time and subsequent session duration
client_untracked_times = df.groupby('client_name')[['untracked_time', 'duration_seconds']].mean()

# Print findings
print(client_untracked_times)
