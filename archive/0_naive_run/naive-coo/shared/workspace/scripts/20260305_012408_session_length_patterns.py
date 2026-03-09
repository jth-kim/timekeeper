"""Investigation: This script investigates the session length patterns by time of day or day of week, providing insight into how session duration varies across different times and days.
Generated: 20260305_012408 UTC
"""

import pandas as pd
from supabase_helper import query_entries

df = pd.DataFrame(query_entries(days=30))

df['start'] = pd.to_datetime(df['start'])

df['hour_of_day'] = df['start'].dt.hour

df['day_of_week'] = df['start'].dt.dayofweek

df['session_length'] = df['duration'] / 3600

daily_avg_session_length = df.groupby('hour_of_day')['session_length'].mean()
weekly_avg_session_length = df.groupby('day_of_week')['session_length'].mean()
print(daily_avg_session_length)
print(weekly_avg_session_length)