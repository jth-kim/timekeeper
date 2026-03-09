"""Investigation: This script investigates the session length patterns by day of the week for each client over the last 14 days, providing insights into how productivity varies across different days and clients.
Generated: 20260305_094830 UTC
"""

import pandas as pd
from supabase_helper import query_entries

days = 14
entries = query_entries(days=days)

data = []
for entry in entries:
    data.append({
        'client': entry['client_name'],
        'day_of_week': pd.to_datetime(entry['start']).dayofweek,
        'session_length': int(pd.to_timedelta(entry['duration']).total_seconds() / 60)
    })

df = pd.DataFrame(data)

grouped_df = df.groupby(['client', 'day_of_week'])['session_length'].mean().reset_index()

print(grouped_df)