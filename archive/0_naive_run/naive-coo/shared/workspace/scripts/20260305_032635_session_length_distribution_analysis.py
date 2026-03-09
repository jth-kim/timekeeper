"""Investigation: This script investigates the distribution of session lengths for each client over the last week and compares it to the overall time allocation targets. It queries the time-tracking data, converts it to a pandas dataframe, calculates session lengths, groups by client, and calculates mean session lengths.
Generated: 20260305_032635 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query time-tracking data for the last week
entries = query_entries(days=7)

# Convert data to a pandas dataframe
df = pd.DataFrame(entries)

# Calculate session lengths in seconds
df['duration'] = pd.to_timedelta(df['duration'])
df['session_length'] = df['duration'].dt.total_seconds()

# Group by client and calculate mean session length
mean_session_lengths = df.groupby('client_name')['session_length'].mean()

# Print the results
print(mean_session_lengths)
