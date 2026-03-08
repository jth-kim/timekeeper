"""Investigation: This script investigates the patterns of time allocation across different days of the week to understand how the Sovereign's schedule varies and whether these variations align with long-term goals.
Generated: 20260305_034301 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query recent entries
entries = query_entries(days=30)

# Convert to DataFrame
df = pd.DataFrame(entries)

# Ensure 'start' column is datetime
df['start'] = pd.to_datetime(df['start'])

# Extract day of week from 'start'
df['day_of_week'] = df['start'].dt.day_name()

# Group by client and day of week, calculate total duration
weekly_allocation = df.groupby(['client_name', 'day_of_week'])['duration'].sum().reset_index()

# Print findings
print(weekly_allocation)
