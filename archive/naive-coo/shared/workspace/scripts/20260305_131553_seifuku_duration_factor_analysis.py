"""Investigation: This script investigates the factors contributing to SEIFUKU's high duration by analyzing recent entries, calculating average session lengths, and assessing their impact on overall time allocation against target priorities.
Generated: 20260305_131553 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent entries for SEIFUKU
entries = query_entries(days=14, client='SEIFUKU')

# Convert to DataFrame
df = entries_to_dataframe(entries)

# Calculate average session length for SEIFUKU
average_session_length_seifuku = df['duration_seconds'].mean()

# Print result
print(f'Average session length for SEIFUKU: {average_session_length_seifuku} seconds')
