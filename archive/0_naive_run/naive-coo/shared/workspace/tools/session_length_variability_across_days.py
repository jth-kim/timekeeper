"""Investigation: This script investigates the patterns of session length variability across different days of the week for each client over the last 14 days, providing insights into how productivity varies across different days and clients.
Generated: 20260305_115514 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent entries
entries = query_entries(days=14)

# Convert to DataFrame
df = entries_to_dataframe(entries)

# Ensure 'start' column is datetime
df['start'] = pd.to_datetime(df['start'])

# Extract day of week from 'start'
df['day_of_week'] = df['start'].dt.day_name()

# Group by client and day of week, calculate mean session length
session_length_variability = df.groupby(['client_name', 'day_of_week'])['duration_seconds'].mean().reset_index()

# Print findings
print(session_length_variability)
