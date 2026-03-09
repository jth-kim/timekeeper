"""Investigation: This script investigates the underlying causes of SEIFUKU's longer average session durations compared to other clients and analyzes how these differences impact overall time allocation against target priorities.
Generated: 20260305_161642 UTC
"""


import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds

# Query recent entries for SEIFUKU
seifuku_entries = [entry for entry in query_entries(days=14) if entry['client_name'] == 'SEIFUKU']

# Convert durations to seconds
for entry in seifuku_entries:
    entry['duration_seconds'] = parse_duration_seconds(entry['duration'])

# Calculate average session duration for SEIFUKU
seifuku_avg_session_duration = sum(entry['duration_seconds'] for entry in seifuku_entries) / len(seifuku_entries)

# Print the result
print(f'SEIFUKU average session duration: {seifuku_avg_session_duration} seconds')

# Query recent entries for other clients
other_client_entries = [entry for entry in query_entries(days=14) if entry['client_name'] != 'SEIFUKU']

# Convert durations to seconds
for entry in other_client_entries:
    entry['duration_seconds'] = parse_duration_seconds(entry['duration'])

# Calculate average session duration for other clients
other_clients_avg_session_durations = {}
for client_name in set(entry['client_name'] for entry in other_client_entries):
    client_entries = [entry for entry in other_client_entries if entry['client_name'] == client_name]
    avg_session_duration = sum(entry['duration_seconds'] for entry in client_entries) / len(client_entries)
    other_clients_avg_session_durations[client_name] = avg_session_duration

# Print the results
for client_name, avg_session_duration in other_clients_avg_session_durations.items():
    print(f'{client_name} average session duration: {avg_session_duration} seconds')

# Compare SEIFUKU's average session duration to other clients
print('Comparison of average session durations:')
for client_name, avg_session_duration in other_clients_avg_session_durations.items():
    print(f'SEIFUKU vs {client_name}: {seifuku_avg_session_duration - avg_session_duration} seconds difference')
