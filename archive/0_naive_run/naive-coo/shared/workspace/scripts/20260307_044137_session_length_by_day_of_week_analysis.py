"""Investigation: This script investigates the session length patterns by day of the week for each client over the last 14 days, providing insights into how productivity varies across different days and clients.
Generated: 20260307_044137 UTC
"""


import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds

# Query entries from the last 14 days
entries = query_entries(days=14)

# Convert entries to a DataFrame with proper types
df = pd.DataFrame(entries)
df['start'] = pd.to_datetime(df['start'])
df['day_of_week'] = df['start'].dt.day_name()

# Parse duration seconds
df['duration_seconds'] = df['duration'].apply(parse_duration_seconds)

# Group by client and day of week, calculate mean session length
session_lengths = df.groupby(['client_name', 'day_of_week'])['duration_seconds'].mean().reset_index()

# Print the results
print(session_lengths)
