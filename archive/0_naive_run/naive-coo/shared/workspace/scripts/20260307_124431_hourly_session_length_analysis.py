"""Investigation: This script investigates the hourly patterns of session lengths for each client over the last week, aiming to understand how productivity varies across different hours and clients. By analyzing recent time-tracking data and calculating mean session lengths for each hour of the day, it provides insights into potential imbalances or patterns in time allocation.
Generated: 20260307_124431 UTC
"""


import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds, entries_to_dataframe

# Query recent time-tracking data
entries = query_entries(days=7)

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate session length in hours and add as new column
df['session_length_hours'] = df['duration_seconds'].apply(lambda x: x / 3600)

# Group by client and hour of day, calculate mean session length
hourly_session_lengths = df.groupby([pd.Grouper(key='start', freq='H'), 'client_name'])['session_length_hours'].mean().reset_index()

# Print the results
print(hourly_session_lengths)
