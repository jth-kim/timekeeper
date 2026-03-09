"""Investigation: This script investigates the factors contributing to the variability in session lengths across different clients over the last two weeks, providing insights into potential imbalances or patterns that could inform adjustments to priorities or alert thresholds.
Generated: 20260306_222250 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data
entries = query_entries(days=14)

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate session lengths in seconds
df['session_length_seconds'] = df['duration_seconds']

# Group by client and calculate mean session length
mean_session_lengths = df.groupby('client_name')['session_length_seconds'].mean()

# Print results
print(mean_session_lengths)
