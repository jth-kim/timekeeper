"""Investigation: This script investigates the factors contributing to the variability in session lengths across clients, providing insights into potential imbalances or patterns that could inform adjustments to priorities or alert thresholds.
Generated: 20260306_165139 UTC
"""


import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds

# Query recent entries (e.g., last 30 days)
entries = query_entries(days=30)

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Group by client and calculate mean session length
mean_session_lengths = df.groupby('client_name')['duration_seconds'].mean()

# Print the results
print(mean_session_lengths)
