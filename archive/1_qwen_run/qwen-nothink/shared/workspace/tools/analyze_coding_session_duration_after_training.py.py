"""Investigation: This script investigates whether the critical workflow pattern (training → coding) identified in recent analysis translates to sustained focus in the coding session itself. By comparing duration of coding sessions immediately following training (vs. those not preceded by training), we uncover if the shorter gap correlates with deeper engagement. The findings will validate whether training serves as a true focus catalyst (not just reducing idle time), directly informing our priority to maximize training→coding sequences. This moves beyond gap analysis to measure actual output quality through session duration patterns.
Generated: 20260308_121729 UTC
"""

from supabase_helper import query_entries, entries_to_dataframe
from datetime import timedelta

# Query last 30 days of entries
entries = query_entries(days=30)
df = entries_to_dataframe(entries)

df['prev_session_type'] = None

def get_prev_session_type(row):
    # Find previous session in chronological order
    prev_row = df[df['start'] < row['start']].sort_values('start', ascending=False).head(1)
    if not prev_row.empty and '⚡️ Training' in prev_row['tags'].values[0]:
        return 'training'
    return 'non-training'

df['prev_session_type'] = df.apply(get_prev_session_type, axis=1)

df_coding = df[df['tags'].apply(lambda tags: '👾 Coding' in tags) & ~df['prev_session_type'].isna()]

df_training_preceded = df_coding[df_coding['prev_session_type'] == 'training']
df_non_training_preceded = df_coding[df_coding['prev_session_type'] == 'non-training']

# Calculate average duration in minutes
avg_training_preceded = df_training_preceded['duration_minutes'].mean()
avg_non_training_preceded = df_non_training_preceded['duration_minutes'].mean()

# Output results
print(f"{'='*50}")
print(f"CODING SESSION DURATION ANALYSIS (n={len(df_coding)})")
print(f"{'='*50}")
print(f"- Coding sessions preceded by training: {len(df_training_preceded)} sessions")
print(f"  Avg duration: {avg_training_preceded:.1f} minutes")
print(f"- Coding sessions not preceded by training: {len(df_non_training_preceded)} sessions")
print(f"  Avg duration: {avg_non_training_preceded:.1f} minutes")
print(f"\
Difference: {avg_training_preceded - avg_non_training_preceded:.1f} minutes (\u2191 {((avg_training_preceded - avg_non_training_preceded)/avg_non_training_preceded)*100:.1f}% longer)")
print(f"{'='*50}")