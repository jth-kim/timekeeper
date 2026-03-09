"""Investigation: This script investigates the factors contributing to the variability in session lengths across different clients over the last two weeks, providing insights into potential imbalances or patterns that could inform adjustments to priorities or alert thresholds.
Generated: 20260305_231122 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent entries (last 14 days)
entries = query_entries(days=14)

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate mean session lengths and standard deviations for each client
client_session_lengths = df.groupby('client_name')['duration_seconds'].agg(['mean', 'std'])

# Print findings
print(client_session_lengths)
