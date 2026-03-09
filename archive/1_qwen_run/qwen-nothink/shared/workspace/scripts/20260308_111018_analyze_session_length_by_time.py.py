"""Investigation: This script analyzes session start times to identify patterns in session length by hour. It helps determine if the Sovereign's focus (as measured by session length) is more consistent at certain times of day, which could inform scheduling decisions for higher productivity. This is a new angle not previously investigated.
Generated: 20260308_111018 UTC
"""

from supabase_helper import query_entries, entries_to_dataframe
import pandas as pd

# Get entries for last 7 days
entries = query_entries(days=7)
df = entries_to_dataframe(entries)

df['start_hour'] = df['start'].dt.hour

hourly_avg = df.groupby('start_hour')['duration_minutes'].mean().reset_index()

print('Session length by start hour (average duration in minutes):')
print('Hour\	Average Duration (min)')
for idx, row in hourly_avg.iterrows():
    print(f'{int(row[\'start_hour\'])}\	{row[\'duration_minutes\']:2f}')