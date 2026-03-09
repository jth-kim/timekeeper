"""Investigation: This investigation moves beyond session-level patterns to analyze day-level strategic allocation, specifically testing if training days (BBOY presence) correlate with higher strategic focus (STAR+SEIFUKU) relative to non-strategic work. Previous analyses focused on session sequencing or description patterns, but this examines the fundamental rhythm of work allocation across days. The findings will determine if scheduling training (BBOY) is an effective strategy for achieving strategic targets (55% allocation), directly informing whether to prioritize BBOY sessions as catalysts for strategic work. It addresses a critical gap in our operational rhythm understanding: does the *presence* of training on a day drive the *composition* of that day's work?
Generated: 20260308_222521 UTC
"""

from supabase_helper import query_entries, entries_to_dataframe
import pandas as pd

# Query last 30 days of entries
entries = query_entries(days=30)
df = entries_to_dataframe(entries)

df['day'] = df['start'].dt.date

df['project_category'] = df['project_name'].map({
    'STAR': 'strategic',
    'SEIFUKU': 'strategic',
    'BBOY': 'training',
    'BOJ': 'non_strategic'
})

day_stats = df.groupby('day').agg(
    total_time=('duration_seconds', 'sum'),
    strategic_time=('duration_seconds', lambda x: x[df['project_category']=='strategic'].sum()),
    training_time=('duration_seconds', lambda x: x[df['project_category']=='training'].sum()),
    non_strategic_time=('duration_seconds', lambda x: x[df['project_category']=='non_strategic'].sum())
).reset_index()

day_stats['strategic_ratio'] = day_stats['strategic_time'] / day_stats['total_time']

day_stats['has_bboy'] = day_stats['training_time'] > 0

bboy_days = day_stats[day_stats['has_bboy']]
non_bboy_days = day_stats[~day_stats['has_bboy']]

print(f"Days with BBOY sessions: {len(bboy_days)}")
print(f"Days without BBOY sessions: {len(non_bboy_days)}")
print(f"\
Average strategic ratio on BBOY days: {bboy_days['strategic_ratio'].mean():.2%}")
print(f"Average strategic ratio on non-BBOY days: {non_bboy_days['strategic_ratio'].mean():.2%}")
print(f"\
Average BBOY time on BBOY days: {bboy_days['training_time'].mean()/3600:.1f} hours")

# Calculate target alignment
strategic_target = 0.55
bboy_target = 0.20

bboy_target_ratio = bboy_days['training_time'].mean() / bboy_days['total_time'].mean()
print(f"\
BBOY time as % of day on BBOY days: {bboy_target_ratio:.2%}")
print(f"Strategic target: {strategic_target:.0%}")
print(f"Strategic ratio on BBOY days vs target: {bboy_days['strategic_ratio'].mean():.2%} vs {strategic_target:.0%}")