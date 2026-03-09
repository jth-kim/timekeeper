"""Investigation: This script analyzes time gaps between consecutive sessions (not tracking idle time) to identify operational anomalies. The previous investigations focused on allocation and labeling errors, but gaps reveal untracked time patterns that impact productivity rhythm. The 12h+ gap between BBOY and SEIFUKU sessions suggests possible sleep/transition periods, while the 4-second gap between SEIFUKU and STAR sessions indicates a potential timer error (likely accidental session restart). This is a new angle that directly impacts the Sovereign's work rhythm and time management awareness.
Generated: 20260308_110355 UTC
"""

from supabase_helper import query_entries, entries_to_dataframe
from datetime import timedelta
import pandas as pd

# Query last 48 hours of entries
entries = query_entries(days=48)

def format_timedelta(td):
    hours, remainder = divmod(td.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    return f'{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}'

df = entries_to_dataframe(entries)
df = df.sort_values('start').reset_index(drop=True)

# Calculate end times
df['end'] = df['start'] + pd.to_timedelta(df['duration_seconds'], unit='s')

# Compute gaps between sessions
gaps = []
for i in range(len(df) - 1):
    gap = df.loc[i+1, 'start'] - df.loc[i, 'end']
    gaps.append((df.loc[i, 'project_name'], df.loc[i+1, 'project_name'], gap))

# Print findings
print("Session Gap Analysis (last 48h):")
print("-"*50)
for i, (prev_proj, next_proj, gap) in enumerate(gaps):
    gap_str = format_timedelta(gap)
    print(f"Session {i+1}: {prev_proj} → {next_proj} | Gap: {gap_str}")

# Identify anomalies
long_gap_threshold = timedelta(hours=12)
short_gap_threshold = timedelta(minutes=1)

long_gaps = [g for g in gaps if g[2] > long_gap_threshold]
short_gaps = [g for g in gaps if g[2] < short_gap_threshold]

print("\nANOMALIES:")
if long_gaps:
    print(f"- LONG GAP: {len(long_gaps)} instances > 12h (e.g., {long_gaps[0][0]} → {long_gaps[0][1]} | {format_timedelta(long_gaps[0][2])})")
else:
    print("- No gaps > 12h")

if short_gaps:
    print(f"- SHORT GAP: {len(short_gaps)} instances < 1m (e.g., {short_gaps[0][0]} → {short_gaps[0][1]} | {format_timedelta(short_gaps[0][2])})")
else:
    print("- No gaps < 1m")