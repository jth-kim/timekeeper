"""Investigation: This script calculates the daily session length variability across different days of the week for each client over the last 14 days, providing insights into potential patterns in time allocation that could impact overall productivity and goal alignment.
Generated: 20260307_094946 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data
entries = query_entries(days=14)

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Group by client and day of week, calculate mean session length
daily_session_lengths = df.groupby([pd.Grouper(key='start', freq='D'), 'client_name'])['duration_seconds'].mean().reset_index()

# Calculate daily session length variability across different days of the week for each client
session_length_variability = daily_session_lengths.groupby('client_name')['duration_seconds'].std().reset_index()

# Print findings
print(session_length_variability)
