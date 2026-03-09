"""Investigation: This script investigates the steps needed to convert the 'duration' column in the dataframe from string format (HH:MM:SS) to a numeric format (seconds), enabling calculations such as mean duration for each client. It queries recent time-tracking data, converts it into a pandas DataFrame, defines a function to convert duration strings to seconds, applies this conversion to the 'duration' column, and calculates the mean duration for each client.
Generated: 20260305_052941 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query recent entries
entries = query_entries(days=14)

# Convert to DataFrame
df = pd.DataFrame(entries)

# Function to convert duration string to seconds
def duration_to_seconds(duration_str):
    h, m, s = map(int, duration_str.split(':'))
    return h * 3600 + m * 60 + s

# Apply conversion function to 'duration' column
df['duration_seconds'] = df['duration'].apply(duration_to_seconds)

# Calculate mean duration for each client
mean_durations = df.groupby('client_name')['duration_seconds'].mean()

print(mean_durations)
