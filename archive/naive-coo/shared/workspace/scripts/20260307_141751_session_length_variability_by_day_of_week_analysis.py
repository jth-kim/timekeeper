"""Investigation: This script investigates the patterns of session length variability across different days of the week for each client over the last 14 days, providing insights into how productivity varies across different days and clients.
Generated: 20260307_141751 UTC
"""


import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds

# Query entries for the last 14 days
entries = query_entries(days=14)

# Convert entries to a DataFrame with proper types
df = pd.DataFrame(entries)
df['start'] = pd.to_datetime(df['start'])
df['stop'] = pd.to_datetime(df['stop'])

# Calculate session length in seconds
df['duration_seconds'] = df['duration'].apply(parse_duration_seconds)

# Group by client and day of week, calculate mean session length
session_length_variability = df.groupby([pd.Grouper(key='start', freq='D'), 'client_name'])['duration_seconds'].mean().reset_index()

# Print the results
print(session_length_variability)
