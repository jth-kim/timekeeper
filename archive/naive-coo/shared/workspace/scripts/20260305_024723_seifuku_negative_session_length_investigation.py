"""Investigation: This script investigates the cause of the negative average session length for SEIFUKU and its impact on overall time allocation by analyzing recent time-tracking data, converting durations to numeric values, filtering for SEIFUKU entries, calculating the average session length, checking for non-numeric durations, and printing findings.
Generated: 20260305_024723 UTC
"""

import pandas as pd
from supabase_helper import query_entries

df = pd.DataFrame(query_entries(days=30))
seifuku_df = df[df['client_name'] == 'SEIFUKU']
seifuku_durations = seifuku_df['duration']

# Convert durations to numeric values (seconds)
seifuku_durations_numeric = pd.to_numeric(seifuku_durations, errors='coerce')

# Calculate average session length for SEIFUKU
average_session_length_seifuku = seifuku_durations_numeric.mean()

print('Average session length for SEIFUKU:', average_session_length_seifuku)

# Check for non-numeric durations
non_numeric_durations = seifuku_durations[seifuku_durations_numeric.isnull()]
print('Non-numeric durations for SEIFUKU:', non_numeric_durations)