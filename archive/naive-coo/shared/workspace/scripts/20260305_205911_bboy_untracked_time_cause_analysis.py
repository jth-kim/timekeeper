"""Investigation: This script investigates the client-level factors contributing to the high untracked time for BBOY and analyzes their impact on overall time allocation against target priorities.
Generated: 20260305_205911 UTC
"""


import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds

# Query recent entries for BBOY
entries = query_entries(days=14)
bboy_entries = [entry for entry in entries if entry['client_name'] == 'BBOY']

# Calculate total untracked time for BBOY
untracked_time = 0
for i in range(len(bboy_entries) - 1):
    start_time = pd.to_datetime(bboy_entries[i]['stop'])
    next_start_time = pd.to_datetime(bboy_entries[i+1]['start'])
    untracked_time += (next_start_time - start_time).total_seconds()

# Analyze factors contributing to high untracked time
if untracked_time > 36000:  # 10 hours in seconds
    print('High untracked time for BBOY is likely due to extended breaks or non-work activities.')
else:
    print('Untracked time for BBOY is within normal ranges.')

# Calculate average session length for BBOY
total_session_length = sum(parse_duration_seconds(entry['duration']) for entry in bboy_entries)
average_session_length = total_session_length / len(bboy_entries)

print(f'Average session length for BBOY: {average_session_length} seconds')
