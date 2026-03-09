"""Investigation: This script investigates the underlying causes of SEIFUKU's longer average session durations compared to other clients and assesses their impact on overall time allocation against target priorities.
Generated: 20260305_162646 UTC
"""


import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds

# Query recent entries for SEIFUKU
seifuku_entries = [entry for entry in query_entries(days=14) if entry['client_name'] == 'SEIFUKU']

# Convert durations to seconds and calculate average session duration
seifuku_durations = [parse_duration_seconds(entry['duration']) for entry in seifuku_entries]
average_seifuku_duration = sum(seifuku_durations) / len(seifuku_durations)

# Print the average session duration for SEIFUKU
print(f'Average session duration for SEIFUKU: {average_seifuku_duration} seconds')

# Investigate the causes of longer sessions
long_sessions = [entry for entry in seifuku_entries if parse_duration_seconds(entry['duration']) > average_seifuku_duration * 1.5]
print('Long sessions:')
for session in long_sessions:
    print(session)
