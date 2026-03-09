"""Investigation: This script analyzes whether the timing of training sessions (⚡️ Training) affects subsequent gap patterns. It converts UTC start times to AEDT (UTC+10) to determine if sessions after 4 PM result in longer recovery gaps. Previous gap analysis showed training has the longest average gap (561.6 min), but this investigates if the timing of training (late afternoon vs. earlier) explains the gap pattern. The findings will determine if scheduling training earlier could reduce unnecessary recovery time and improve work rhythm. This is a new angle beyond previous tag-based gap analysis (which didn't consider time of day) and addresses the agenda item about optimizing training session timing.
Generated: 20260308_120904 UTC
"""

from supabase_helper import query_entries, entries_to_dataframe
from datetime import timedelta
import pandas as pd

# Query all entries for the last 30 days
entries = query_entries(days=30)

df = entries_to_dataframe(entries)

df = df.sort_values('start').reset_index(drop=True)

df['gap_minutes'] = (df['start'].shift(-1) - df['stop']).dt.total_seconds() / 60

df['local_start'] = df['start'] + pd.Timedelta(hours=10)  # Convert UTC to AEDT (UTC+10)
df['local_hour'] = df['local_start'].dt.hour

def has_tag(entry, tag):
    return tag in entry.get('tags', [])

df['is_training'] = df.apply(lambda row: has_tag(row, '⚡️ Training'), axis=1)

df_training = df[df['is_training']]

df_training['after_4pm'] = df_training['local_hour'] >= 16

after_4pm = df_training[df_training['after_4pm']]
before_4pm = df_training[~df_training['after_4pm']]

gap_after = after_4pm['gap_minutes'].mean() if not after_4pm.empty else None
gap_before = before_4pm['gap_minutes'].mean() if not before_4pm.empty else None

count_after = len(after_4pm)
count_before = len(before_4pm)

print(f"Training sessions after 4 PM AEDT ({count_after} sessions):")
print(f"  Average gap to next session: {gap_after:.1f} minutes")
print(f"Training sessions before 4 PM AEDT ({count_before} sessions):")
print(f"  Average gap to next session: {gap_before:.1f} minutes")
print(f"\
\
Key insight: {'Training sessions after 4 PM have longer gaps' if gap_after > gap_before else 'Training sessions before 4 PM have longer gaps'}")