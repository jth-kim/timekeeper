"""Investigation: This script investigates the relationship between task-level activities within each client and overall session length variability, considering the impact of client transitions on these activities. It calculates average session lengths for each client and prints the results, providing insights into potential imbalances or patterns that could inform adjustments to priorities or alert thresholds.
Generated: 20260307_030101 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data
entries = query_entries(days=14)

# Convert entries to a DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate session lengths in seconds
df['session_length_seconds'] = df['duration_seconds']

# Group by client and calculate average session length
average_session_lengths = df.groupby('client_name')['session_length_seconds'].mean()

# Print the results
print(average_session_lengths)
