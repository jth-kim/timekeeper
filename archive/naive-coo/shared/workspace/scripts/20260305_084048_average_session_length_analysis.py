"""Investigation: This script calculates the average session lengths for each client over the last week and compares these averages to the overall average session length. The goal is to identify potential imbalances in time allocation between clients.
Generated: 20260305_084048 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query recent time-tracking data
entries = query_entries(days=7)

# Create a DataFrame from the entries
df = pd.DataFrame(entries)

# Convert duration to seconds
def convert_duration_to_seconds(duration):
    hours, minutes, seconds = map(int, duration.split(':'))
    return hours * 3600 + minutes * 60 + seconds

df['duration'] = df['duration'].apply(convert_duration_to_seconds)

# Calculate average session length for each client
average_session_lengths = df.groupby('client_name')['duration'].mean()

# Print the results
print(average_session_lengths)
