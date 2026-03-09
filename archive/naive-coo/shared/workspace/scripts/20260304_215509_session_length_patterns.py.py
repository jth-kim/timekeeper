"""Investigation: This script investigates session length patterns by time of day or day of week to understand how the Sovereign's productivity varies throughout the day and across different days of the week.
Generated: 20260304_215509 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query entries for the last 30 days
entries = query_entries(days=30)

# Convert data to DataFrame
df = pd.DataFrame(entries)

# Ensure 'start' column is of datetime type
df['start'] = pd.to_datetime(df['start'])

# Extract hour of day and day of week from 'start'
df['hour_of_day'] = df['start'].dt.hour
df['day_of_week'] = df['start'].dt.dayofweek

# Calculate session length in minutes
df['session_length_minutes'] = df['duration']

# Group by hour of day or day of week and calculate mean session length
hourly_mean_session_length = df.groupby('hour_of_day')['session_length_minutes'].mean()
daily_mean_session_length = df.groupby('day_of_week')['session_length_minutes'].mean()

# Print results
print('Mean Session Length by Hour of Day:')
print(hourly_mean_session_length)
print('\
Mean Session Length by Day of Week:')
print(daily_mean_session_length)
