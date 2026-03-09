"""Investigation: This script investigates the session length patterns by day of the week for each client over the last 14 days, aiming to understand how productivity varies across different days and clients.
Generated: 20260306_211026 UTC
"""


from supabase_helper import query_entries, entries_to_dataframe
import pandas as pd

# Get recent entries
entries = query_entries(days=14)

# Convert to dataframe
df = entries_to_dataframe(entries)

# Ensure 'start' column is datetime
df['start'] = pd.to_datetime(df['start'])

# Extract day of week from 'start'
df['day_of_week'] = df['start'].dt.day_name()

# Group by client and day of week, calculate mean session length
session_lengths = df.groupby(['client_name', 'day_of_week'])['duration_seconds'].mean().reset_index()

# Print results in a clear format
print(session_lengths.to_string(index=False))
