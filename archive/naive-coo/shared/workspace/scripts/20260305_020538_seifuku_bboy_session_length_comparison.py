"""Investigation: This script compares the average session lengths of SEIFUKU and BBOY over the last two weeks, calculates the difference in their average session lengths, and prints the findings. It helps to understand the underlying causes of the differences in average session lengths between these two clients and how these differences might impact the Sovereign's overall time allocation strategy.
Generated: 20260305_020538 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query recent entries for SEIFUKU and BBOY
entries = query_entries(days=14)
seifuku_entries = [entry for entry in entries if entry['client_name'] == 'SEIFUKU']
bboy_entries = [entry for entry in entries if entry['client_name'] == 'BBOY']

# Convert durations to seconds and calculate average session lengths
def duration_to_seconds(duration):
    hours, minutes, seconds = map(int, duration.split(':'))
    return hours * 3600 + minutes * 60 + seconds

seifuku_durations = [duration_to_seconds(entry['duration']) for entry in seifuku_entries]
bboy_durations = [duration_to_seconds(entry['duration']) for entry in bboy_entries]

seifuku_avg_session_length = sum(seifuku_durations) / len(seifuku_durations)
bboy_avg_session_length = sum(bboy_durations) / len(bboy_durations)

# Print findings
print(f'SEIFUKU average session length: {seifuku_avg_session_length} seconds')
print(f'BBOY average session length: {bboy_avg_session_length} seconds')

# Calculate difference in average session lengths
avg_session_length_diff = seifuku_avg_session_length - bboy_avg_session_length

# Print significance of difference
if avg_session_length_diff > 0:
    print(f'SEIFUKU has an average session length {avg_session_length_diff} seconds longer than BBOY')
elif avg_session_length_diff < 0:
    print(f'BBOY has an average session length {abs(avg_session_length_diff)} seconds longer than SEIFUKU')
else:
    print('SEIFUKU and BBOY have the same average session length')
