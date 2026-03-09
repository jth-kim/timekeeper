"""Investigation: This script converts the 'start' and 'stop' columns to a datetime format, calculates session lengths in seconds, and then calculates untracked times between sessions in seconds. It provides a foundation for further analyses on time allocation patterns and potential imbalances.
Generated: 20260305_065803 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query recent time-tracking data
entries = query_entries(days=14)

# Create a pandas DataFrame from the entries
df = pd.DataFrame(entries)

# Convert 'start' and 'stop' columns to datetime format
df['start'] = pd.to_datetime(df['start'])
df['stop'] = pd.to_datetime(df['stop'])

# Calculate session lengths in seconds
df['session_length_seconds'] = (df['stop'] - df['start']).dt.total_seconds()

# Calculate untracked times between sessions in seconds
df['untracked_time_seconds'] = (df['start'].shift(-1) - df['stop']).dt.total_seconds()

# Print the resulting DataFrame
print(df)
