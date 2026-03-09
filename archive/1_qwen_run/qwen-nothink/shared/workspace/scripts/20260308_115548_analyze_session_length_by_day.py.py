"""Investigation: This script analyzes session duration patterns by day of week, moving beyond project types and tags to reveal temporal work rhythms. It's the first investigation to correlate time-of-day patterns with session length, which could indicate energy management habits (e.g., longer sessions on focused days). Unlike previous tag-based analyses, this uses raw temporal data to uncover systemic patterns. The findings will help determine if the Sovereign's work schedule aligns with natural energy cycles, addressing a gap in our understanding of 'when' work happens versus 'what' work happens. This is critical because current data shows Sunday (local time) as an active work day despite being weekend - suggesting potential misalignment with recovery cycles.
Generated: 20260308_115548 UTC
"""

from supabase_helper import query_entries, entries_to_dataframe
from datetime import datetime
import pandas as pd

# Query last 30 days of entries
entries = query_entries(days=30)
if not entries:
    print('No entries found for analysis')
    exit()

# Convert to DataFrame with proper duration handling
df = entries_to_dataframe(entries)

# Extract day of week (0=Monday, 6=Sunday)
df['day_of_week'] = df['start'].dt.dayofweek

# Map to human-readable day names
weekday_map = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
df['day_name'] = df['day_of_week'].map(weekday_map)

day_analysis = df.groupby('day_name').agg(
    sessions=('start', 'count'),
    avg_duration_minutes=('duration_minutes', 'mean')
).reset_index()

day_analysis = day_analysis.sort_values('day_name')

# Format output
print("Session Length Patterns by Day of Week (Last 30 Days)")
print("===============================================")
for _, row in day_analysis.iterrows():
    print(f"{row['day_name']}: {row['sessions']} sessions, {row['avg_duration_minutes']:.1f} min avg")

# Check for significant variations
max_day = day_analysis.loc[day_analysis['avg_duration_minutes'].idxmax()]
min_day = day_analysis.loc[day_analysis['avg_duration_minutes'].idxmin()]

print(f"\
Peak productivity day: {max_day['day_name']} ({max_day['avg_duration_minutes']:.1f} min)")
print(f"Lowest productivity day: {min_day['day_name']} ({min_day['avg_duration_minutes']:.1f} min)")