"""Investigation: This script investigates the factors contributing to the high untracked time for BBOY and calculates the average untracked time between BBOY sessions. By analyzing these factors, we can identify potential distractions or unnoticed patterns that could impact overall time allocation.
Generated: 20260306_162831 UTC
"""


from supabase_helper import query_entries, parse_duration_seconds
import pandas as pd

# Query recent entries for BBOY
entries = query_entries(days=14)
bboy_entries = [entry for entry in entries if entry['client_name'] == 'BBOY']

# Convert to DataFrame and calculate session lengths
df = pd.DataFrame(bboy_entries)
df['duration_seconds'] = df['duration'].apply(parse_duration_seconds)

# Calculate total time spent on BBOY tasks
total_bboy_time = df['duration_seconds'].sum()

# Calculate average session length for BBOY
avg_session_length = df['duration_seconds'].mean()

# Investigate gaps between sessions (untracked time)
gaps = []
for i in range(len(bboy_entries) - 1):
    gap = bboy_entries[i+1]['start'] - bboy_entries[i]['stop']
    gaps.append(gap.total_seconds())

# Calculate average untracked time
avg_untracked_time = sum(gaps) / len(gaps)

print(f'Total time spent on BBOY tasks: {total_bboy_time} seconds')
print(f'Average session length for BBOY: {avg_session_length} seconds')
print(f'Average untracked time between BBOY sessions: {avg_untracked_time} seconds')
