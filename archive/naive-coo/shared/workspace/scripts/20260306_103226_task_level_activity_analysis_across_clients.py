"""Investigation: This script investigates task-level activities within each client that contribute to session length variability and assesses their alignment with the Sovereign's long-term objectives. It calculates mean session lengths for each task within each client, providing insights into potential imbalances or patterns that could inform adjustments to priorities or alert thresholds.
Generated: 20260306_103226 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data
entries = query_entries(days=14)

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate session length in seconds for each entry
df['session_length_seconds'] = df['duration_seconds']

# Group by client and project, calculate mean session length
mean_session_lengths = df.groupby(['client_name', 'project_name'])['session_length_seconds'].mean().reset_index()

# Print results
print(mean_session_lengths)
