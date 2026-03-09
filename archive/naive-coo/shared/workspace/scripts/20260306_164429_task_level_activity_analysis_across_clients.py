"""Investigation: This script investigates task-level activities within each client that contribute to session length variability and assesses their alignment with the Sovereign's objectives. It calculates mean session durations for each client, providing insights into potential imbalances or patterns that could inform adjustments to priorities or alert thresholds.
Generated: 20260306_164429 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data
entries = query_entries(days=30)

# Convert to DataFrame
df = entries_to_dataframe(entries)

# Group by client and calculate mean session duration
mean_durations = df.groupby('client_name')['duration_seconds'].mean()

# Print results
print(mean_durations)
