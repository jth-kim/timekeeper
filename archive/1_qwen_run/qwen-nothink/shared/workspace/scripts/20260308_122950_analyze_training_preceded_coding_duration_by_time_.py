"""Investigation: This script investigates whether the observed 8.1-minute duration increase in training-preceded coding sessions (from previous investigation) persists when controlling for time of day. It compares morning (9am-12pm) and afternoon (1pm-5pm) sessions separately. The analysis reveals whether the focus continuity effect is consistent across work rhythms or if it's driven by specific time blocks. This directly tests the agenda item about training→coding quality correlation while accounting for natural energy fluctuations. The small sample size (n=7 training-preceded) necessitates time-block analysis to avoid misinterpreting noise as pattern.
Generated: 20260308_122950 UTC
"""

from supabase_helper import query_entries, entries_to_dataframe
from datetime import timedelta

# Get last 30 days of data
entries = query_entries(days=30)
df = entries_to_dataframe(entries)

df = df.sort_values('start').reset_index(drop=True)

# Add next session info
next_start = df['start'].shift(-1)
next_tags = df['tags'].shift(-1)
df['next_start'] = next_start
df['next_tags'] = next_tags

df = df.dropna(subset=['next_start', 'next_tags'])

# Filter for training → coding sequences (immediate next session)
training_preceded = df[
    df['tags'].apply(lambda tags: '⚡️ Training' in tags) & 
    df['next_tags'].apply(lambda tags: '👾 Coding' in tags)
]

def get_time_block(start):
    # Convert UTC start to AEDT (UTC+10)
    aedt = start + timedelta(hours=10)
    hour = aedt.hour
    if 9 <= hour < 12:
        return 'Morning'
    elif 12 <= hour < 17:
        return 'Afternoon'
    else:
        return 'Other'

# Classify training-preceded coding sessions by time block
training_preceded['time_block'] = training_preceded['next_start'].apply(get_time_block)

# Get non-preceded coding sessions (coding not immediately after training)
non_preceded = df[
    df['tags'].apply(lambda tags: '👾 Coding' in tags) & 
    ~df['prev_tags'].apply(lambda tags: '⚡️ Training' in tags)  # Previous session not training
]
non_preceded['time_block'] = non_preceded['start'].apply(get_time_block)

# Calculate averages by time block
results = []
for block in ['Morning', 'Afternoon']:
    t_preceded = training_preceded[training_preceded['time_block'] == block]
    n_preceded = non_preceded[non_preceded['time_block'] == block]
    
    t_avg = t_preceded['duration_minutes'].mean() if not t_preceded.empty else None
    n_avg = n_preceded['duration_minutes'].mean() if not n_preceded.empty else None
    
    results.append({
        'time_block': block,
        'training_preceded_avg': t_avg,
        'training_preceded_count': len(t_preceded),
        'non_preceded_avg': n_avg,
        'non_preceded_count': len(n_preceded)
    })

# Print findings
print("\
Analysis: Training-Preceded Coding Sessions Duration by Time of Day\
" + "="*50)
print("{'Time Block': 10s} | {'T-Preceded Avg (min)': 20s} | {"Count": 10s} | {'Non-Preceded Avg (min)': 20s} | {"Count": 10s}")
print("="*50)
for r in results:
    t_avg = f"{r['training_preceded_avg']:.1f}" if r['training_preceded_avg'] else 'N/A'
    n_avg = f"{r['non_preceded_avg']:.1f}" if r['non_preceded_avg'] else 'N/A'
    
    print(f"{r['time_block']:10s} | {t_avg:20s} | {r['training_preceded_count']:10d} | {n_avg:20s} | {r['non_preceded_count']:10d}")

# Calculate overall difference
overall_t_avg = training_preceded['duration_minutes'].mean() if not training_preceded.empty else None
overall_n_avg = non_preceded['duration_minutes'].mean() if not non_preceded.empty else None

diff = overall_t_avg - overall_n_avg if overall_t_avg and overall_n_avg else None

print(f"\
Overall difference (training-preceded vs non-preceded): {diff:.1f} minutes (n={len(training_preceded)} vs {len(non_preceded)})")