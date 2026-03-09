"""Investigation: This script analyzes the time gaps between consecutive sessions (untracked time) to uncover break patterns. Unlike previous investigations that focused on session content, this reveals whether breaks are intentional (e.g., longer gaps after coding sessions) or accidental. The findings will directly inform energy management strategies by showing if the Sovereign structures recovery time after high-focus work. Critical for validating if the observed training sessions (⚡️) are scheduled as recovery after coding (👾) - a pattern not yet verified through gap analysis.
Generated: 20260308_120457 UTC
"""

from supabase_helper import query_entries, entries_to_dataframe
import pandas as pd
from datetime import timedelta

# Get last 30 days of entries
entries = query_entries(days=30)
if not entries:
    print("No entries found for last 30 days")
    exit()

df = entries_to_dataframe(entries)
df = df.sort_values('start').reset_index(drop=True)

# Calculate gaps between consecutive sessions (in minutes)
df['gap_minutes'] = (df['start'] - df['stop'].shift(1)).dt.total_seconds() / 60

df['gap_minutes'] = df['gap_minutes'].apply(lambda x: max(0, x))  # Ignore negative gaps

gap_stats = {
    'avg_gap_minutes': df['gap_minutes'].mean(),
    'median_gap_minutes': df['gap_minutes'].median(),
    'max_gap_minutes': df['gap_minutes'].max(),
    'min_gap_minutes': df['gap_minutes'].min(),
    'total_gaps': len(df) - 1
}

# Analyze gaps by session type (using tags)
def get_session_type(tags):
    if '👾 Coding' in tags:
        return 'Coding'
    elif '⚡️ Training' in tags:
        return 'Training'
    else:
        return 'Other'

df['session_type'] = df['tags'].apply(get_session_type)

gap_by_type = df.groupby('session_type')['gap_minutes'].agg(['mean', 'median', 'count']).reset_index()

# Analyze gaps by day of week
if not df.empty:
    df['day_of_week'] = df['start'].dt.day_name()
    gap_by_day = df.groupby('day_of_week')['gap_minutes'].agg(['mean', 'median', 'count']).reset_index()
else:
    gap_by_day = pd.DataFrame()

# Print findings
print("===== Session Gap Analysis (Last 30 Days) =====")
print(f"Total gaps analyzed: {gap_stats['total_gaps']}")
print(f"Average gap: {gap_stats['avg_gap_minutes']:.1f} min | Median: {gap_stats['median_gap_minutes']:.1f} min")
print(f"Longest gap: {gap_stats['max_gap_minutes']:.1f} min | Shortest: {gap_stats['min_gap_minutes']:.1f} min")

print("\
===== By Session Type =====")
for _, row in gap_by_type.iterrows():
    print(f"{row['session_type']}: avg gap {row['mean']:.1f} min (n={row['count']})")

print("\
===== By Day of Week =====")
for _, row in gap_by_day.iterrows():
    print(f"{row['day_of_week']}: avg gap {row['mean']:.1f} min (n={row['count']})")