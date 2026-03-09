"""Investigation: This script investigates the patterns of session lengths and task-level activities within each client across different days of the week, providing insights into how productivity varies across different days and clients. By analyzing recent time-tracking data and calculating mean session lengths for each client by day of the week, it aims to understand how these patterns impact overall time allocation against target priorities.
Generated: 20260307_222623 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent entries
entries = query_entries(days=14)

# Convert to DataFrame
df = entries_to_dataframe(entries)

# Group by client and day of week
grouped_df = df.groupby([pd.Grouper(key='start', freq='D'), 'client_name'])

# Calculate mean session length for each group
mean_session_lengths = grouped_df['duration_seconds'].mean().reset_index()

# Print results
print(mean_session_lengths)
