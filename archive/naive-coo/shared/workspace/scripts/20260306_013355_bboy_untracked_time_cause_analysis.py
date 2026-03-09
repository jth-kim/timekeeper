"""Investigation: This script investigates the factors contributing to the high untracked time for BBOY and assesses its impact on overall time allocation against target priorities.
Generated: 20260306_013355 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query recent entries for BBOY
entries = query_entries(days=14)
bboy_entries = [entry for entry in entries if entry['client_name'] == 'BBOY']

# Convert to DataFrame
df = pd.DataFrame(bboy_entries)

# Calculate total time spent on BBOY tasks
total_bboy_time = df['duration'].apply(parse_duration_seconds).sum()

# Calculate untracked time between sessions
untracked_time = []
for i in range(len(df) - 1):
    session_end = df.iloc[i]['stop']
    next_session_start = df.iloc[i+1]['start']
    untracked_time.append((next_session_start - session_end).total_seconds())

# Calculate average untracked time
avg_untracked_time = sum(untracked_time) / len(untracked_time)

# Print findings
print(f'Total time spent on BBOY tasks: {total_bboy_time} seconds')
print(f'Average untracked time between BBOY sessions: {avg_untracked_time} seconds')