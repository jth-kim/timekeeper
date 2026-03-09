"""Investigation: This script investigates the factors contributing to SEIFUKU's high duration by analyzing recent entries, calculating average session lengths, and modifying the query_entries function to include client filtering.
Generated: 20260305_125108 UTC
"""


import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds

def query_entries_with_client_filtering(days, client=None):
    entries = query_entries(days)
    if client:
        filtered_entries = [entry for entry in entries if entry['client_name'] == client]
        return filtered_entries
    else:
        return entries

# Get SEIFUKU entries from the last 14 days
seifuku_entries = query_entries_with_client_filtering(14, 'SEIFUKU')

# Convert durations to seconds and calculate average session length for SEIFUKU
average_session_length_seifuku = sum(parse_duration_seconds(entry['duration']) for entry in seifuku_entries) / len(seifuku_entries)

print(f'Average session length for SEIFUKU: {average_session_length_seifuku} seconds')
