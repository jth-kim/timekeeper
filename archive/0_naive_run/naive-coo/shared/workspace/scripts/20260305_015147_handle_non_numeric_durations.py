"""Investigation: This script investigates the cause of non-numeric values in the 'duration' column and attempts to convert them into numeric values (seconds) for accurate calculation of average session lengths.
Generated: 20260305_015147 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query entries for the last 30 days
entries = query_entries(days=30)

# Convert the list of dictionaries into a pandas DataFrame
df = pd.DataFrame(entries)

# Identify non-numeric values in the 'duration' column
non_numeric_durations = df[df['duration'].apply(lambda x: not isinstance(x, (int, float)))]

# Print the number of non-numeric durations found
print(f'Non-numeric durations found: {len(non_numeric_durations)}')

# Attempt to convert non-numeric durations to numeric values
def convert_duration_to_seconds(duration):
    if ':' in duration:
        hours, minutes, seconds = map(int, duration.split(':'))
        return hours * 3600 + minutes * 60 + seconds
    else:
        return None

df['duration_in_seconds'] = df['duration'].apply(convert_duration_to_seconds)

# Calculate average session lengths for each client
average_session_lengths = df.groupby('client_name')['duration_in_seconds'].mean()

print(average_session_lengths)
