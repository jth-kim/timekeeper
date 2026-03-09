"""Investigation: This script investigates the factors contributing to the significant variability in session lengths for SEIFUKU across different tasks, such as coding versus managing, and assesses their impact on overall time allocation against target priorities.
Generated: 20260305_060309 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query recent entries for SEIFUKU
entries = query_entries(days=30)
seifuku_entries = [entry for entry in entries if entry['client_name'] == 'SEIFUKU']

# Convert to dataframe
df = pd.DataFrame(seifuku_entries)

# Define a function to convert duration strings to seconds
def duration_to_seconds(duration):
    hours, minutes, seconds = map(int, duration.split(':'))
    return hours * 3600 + minutes * 60 + seconds

# Apply the conversion to the 'duration' column
df['duration_seconds'] = df['duration'].apply(duration_to_seconds)

# Group by task and calculate average session length
average_session_lengths = df.groupby('description')['duration_seconds'].mean()

# Print the results
print(average_session_lengths)
