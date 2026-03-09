"""Investigation: This script investigates the relationship between task-level activities within each client and overall session length variability, aiming to understand how these activities impact time allocation against target priorities. By analyzing recent time-tracking data and calculating mean session lengths for each client, it provides insights into potential imbalances or patterns that could inform adjustments to priorities or alert thresholds.
Generated: 20260307_020126 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent entries
entries = query_entries(days=14)

# Convert to DataFrame
df = entries_to_dataframe(entries)

# Group by client and calculate mean session length
mean_session_lengths = df.groupby('client_name')['duration_seconds'].mean()

# Print results
print(mean_session_lengths)
