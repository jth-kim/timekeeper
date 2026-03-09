"""Investigation: This script analyzes the start time patterns of strategic (STAR/SEIFUKU) vs non-strategic (BBOY/BOJ) sessions across days of week. It identifies whether strategic sessions consistently begin earlier in the day (aligning with optimal cognitive windows) and whether non-strategic sessions cluster in suboptimal hours. This addresses a critical gap in our operational rhythm understanding: strategic work requires deep focus that's typically most effective in morning hours, but our current data shows potential misalignment. The findings will determine if scheduling interventions (e.g., blocking morning slots for STAR) are warranted, directly supporting the alert threshold targets for strategic allocation.
Generated: 20260308_174449 UTC
"""

from supabase_helper import query_entries, entries_to_dataframe
import pandas as pd

# Get all entries from last 30 days
entries = query_entries(days=30)
df = entries_to_dataframe(entries)

df['start_hour'] = df['start'].dt.hour
df['day_of_week'] = df['start'].dt.dayofweek

def get_project_type(row):
    if row['project_name'] in ['STAR', 'SEIFUKU']:
        return 'Strategic (STAR/SEIFUKU)'
    elif row['project_name'] in ['BBOY', 'BOJ']:
        return 'Non-Strategic (BBOY/BOJ)'
    else:
        return 'Other'

df['project_type'] = df.apply(get_project_type, axis=1)

grouped = df.groupby(['project_type', 'day_of_week']).agg(
    avg_start_hour=('start_hour', 'mean'),
    session_count=('start', 'count')
).reset_index()

day_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
grouped['day_of_week'] = grouped['day_of_week'].apply(lambda x: day_names[x])

def format_hours(h):
    if h < 0:
        return 'N/A'
    return f'{int(h):02d}:{int((h % 1) * 60):02d}'

# Format results for readable output
results = []
for _, row in grouped.iterrows():
    if row['session_count'] < 5:  # Skip sparse data
        continue
    results.append(f"{row['project_type']} | {row['day_of_week']} | {format_hours(row['avg_start_hour'])} ({row['session_count']} sessions)")

# Print findings
print("Strategic session start time analysis (last 30 days):")
print("-" * 60)
print("Project Type        | Day       | Avg Start Time (HH:MM) | Sessions")
print("-" * 60)
for line in results:
    print(line)