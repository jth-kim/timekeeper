"""Investigation: This script investigates the weekly time distribution trends across clients over the last 30 days, providing insight into how time allocation varies by client and week.
Generated: 20260305_012038 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query entries for the last 30 days
entries = query_entries(days=30)

# Convert to DataFrame
df = pd.DataFrame(entries)

# Ensure 'start' column is datetime
df['start'] = pd.to_datetime(df['start'])

# Extract week number from 'start' date
df['week'] = df['start'].dt.isocalendar().week

# Group by client and week, sum duration
weekly_duration = df.groupby(['client_name', 'week'])['duration'].sum().reset_index()

# Pivot to get weekly duration for each client
pivoted_df = weekly_duration.pivot(index='week', columns='client_name', values='duration')

# Print the pivoted DataFrame
print(pivoted_df)
