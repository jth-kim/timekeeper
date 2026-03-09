"""Investigation: This script investigates the underlying causes of the variability in session lengths for each client and assesses their impact on overall time allocation against target priorities. It calculates the mean session length for each client and prints the results, providing insights into potential imbalances or patterns that could inform adjustments to alert thresholds configuration.
Generated: 20260307_223940 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data
entries = query_entries(days=14)

# Convert entries to a DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate session lengths in seconds
df['session_length_seconds'] = df['duration_seconds']

# Group by client and calculate mean session length
mean_session_lengths = df.groupby('client_name')['session_length_seconds'].mean()

# Print the results
print(mean_session_lengths)
