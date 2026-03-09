"""Investigation: This script investigates the factors contributing to the session length variability across clients and assesses their impact on overall time allocation. It calculates the average session duration for each client, providing insights into potential imbalances or patterns that could inform adjustments to priorities or alert thresholds.
Generated: 20260306_174516 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent entries
entries = query_entries(days=30)

# Convert to DataFrame
df = entries_to_dataframe(entries)

# Calculate average session duration for each client
avg_session_durations = df.groupby('client_name')['duration_seconds'].mean()

# Print results
print(avg_session_durations)
