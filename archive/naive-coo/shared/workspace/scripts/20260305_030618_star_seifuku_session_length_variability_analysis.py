"""Investigation: This script investigates the underlying causes of the high standard deviations in session lengths for STAR and SEIFUKU, and assesses their impact on overall time allocation against target priorities.
Generated: 20260305_030618 UTC
"""

import pandas as pd
from supabase_helper import query_entries

days = 30
limit = 500
entries = query_entries(days=days, limit=limit)

data = []
for entry in entries:
    client_name = entry['client_name']
    duration = pd.to_timedelta(entry['duration']).total_seconds()
    data.append({'client_name': client_name, 'duration': duration})

df = pd.DataFrame(data)

star_df = df[df['client_name'] == 'STAR']
seifuku_df = df[df['client_name'] == 'SEIFUKU']

star_mean_session_length = star_df['duration'].mean()
star_std_dev = star_df['duration'].std()

seifuku_mean_session_length = seifuku_df['duration'].mean()
seifuku_std_dev = seifuku_df['duration'].std()

print(f'STAR mean session length: {star_mean_session_length} seconds')
print(f'STAR standard deviation: {star_std_dev} seconds')
print(f'SEIFUKU mean session length: {seifuku_mean_session_length} seconds')
print(f'SEIFUKU standard deviation: {seifuku_std_dev} seconds')