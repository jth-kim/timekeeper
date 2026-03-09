"""Investigation: This script investigates the factors contributing to the high average session duration in SEIFUKU and their impact on overall time allocation against target priorities.
Generated: 20260306_115736 UTC
"""


import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds

# Query recent entries for SEIFUKU
entries = query_entries(days=14)
seifuku_entries = [entry for entry in entries if entry['client_name'] == 'SEIFUKU']

# Convert duration to seconds and calculate average session length
durations = [parse_duration_seconds(entry['duration']) for entry in seifuku_entries]
average_session_length = sum(durations) / len(durations)

# Print the result
print(f'Average session length for SEIFUKU: {average_session_length} seconds')
