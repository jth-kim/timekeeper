"""Investigation: This script investigates the cause of the negative average session length for SEIFUKU and its impact on overall time allocation by analyzing recent time-tracking data, converting durations to numeric values, filtering for SEIFUKU entries, calculating the average session length, checking for non-numeric durations, and printing findings. It also performs further investigation if a negative average session length is found.
Generated: 20260305_014739 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query recent entries to analyze session lengths
entries = query_entries(days=30)

# Convert entries to a pandas DataFrame for easier analysis
df = pd.DataFrame(entries)

# Ensure 'duration' column is numeric (seconds) for calculation
df['duration'] = pd.to_numeric(df['duration'], errors='coerce')

# Filter for SEIFUKU entries
seifuku_entries = df[df['client_name'] == 'SEIFUKU']

# Calculate average session length for SEIFUKU
average_session_length_seifuku = seifuku_entries['duration'].mean()

# Check if there are any non-numeric values in the 'duration' column that could cause errors
non_numeric_durations = df[pd.isnull(df['duration'])]

# Print findings
print('Average session length for SEIFUKU:', average_session_length_seifuku)
print('Non-numeric durations:', non_numeric_durations)

# Further investigation based on findings
if average_session_length_seifuku < 0:
    print('Negative average session length found. Investigating further...')
    # Look for patterns or errors in data that could cause negative duration
    error_entries = seifuku_entries[seifuku_entries['duration'] < 0]
    print('Error entries:', error_entries)
else:
    print('Average session length is not negative. No further action needed.')
