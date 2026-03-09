"""Investigation: This script investigates the underlying causes of the discrepancy in BBOY's untracked time and its impact on overall time allocation against target priorities. It calculates the total time spent on BBOY, analyzes the distribution of untracked time between sessions, and investigates potential causes of discrepancy in untracked time.
Generated: 20260305_181051 UTC
"""


import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds

# Query recent entries for BBOY
entries = query_entries(days=14)
bboy_entries = [entry for entry in entries if entry['client_name'] == 'BBOY']

# Convert durations to seconds and calculate total time spent on BBOY
total_bboy_time = sum(parse_duration_seconds(entry['duration']) for entry in bboy_entries)

# Calculate untracked time between sessions
untracked_time = []
for i in range(len(bboy_entries) - 1):
    session_end = pd.to_datetime(bboy_entries[i]['stop'])
    next_session_start = pd.to_datetime(bboy_entries[i+1]['start'])
    untracked_time.append((next_session_start - session_end).total_seconds())

# Analyze the distribution of untracked time
avg_untracked_time = sum(untracked_time) / len(untracked_time)
print(f'Average untracked time between BBOY sessions: {avg_untracked_time} seconds')

# Investigate potential causes of discrepancy in untracked time
discrepancy = total_bboy_time - sum(parse_duration_seconds(entry['duration']) for entry in bboy_entries)
print(f'Discrepancy in BBOY untracked time: {discrepancy} seconds')
