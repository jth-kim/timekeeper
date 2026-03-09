"""Investigation: This script investigates the primary factors contributing to the variability in session lengths across different days of the week for each client and assesses their impact on overall productivity. It calculates mean session lengths for each client by day of the week, providing insights into potential imbalances or patterns that could inform adjustments to priorities or alert thresholds.
Generated: 20260307_160149 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data
entries = query_entries(days=14)

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate session lengths in seconds
df['session_length_seconds'] = df['duration_seconds']

# Group by client and day of week, calculate mean session length
mean_session_lengths = df.groupby(['client_name', pd.Grouper(key='start', freq='D')])['session_length_seconds'].mean().reset_index()

# Print results in a clear format
print(mean_session_lengths)
