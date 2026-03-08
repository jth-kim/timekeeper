"""Investigation: This script investigates the distribution of session lengths for each client over the last week and compares it to the overall time allocation targets. It queries the time-tracking data, converts it to a pandas dataframe, calculates session lengths, groups by client, and calculates mean session lengths.
Generated: 20260305_015541 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query entries for the last week
entries = query_entries(days=7)

# Convert entries to dataframe
df = pd.DataFrame(entries)

# Ensure 'start' and 'stop' columns are datetime
df['start'] = pd.to_datetime(df['start'])
df['stop'] = pd.to_datetime(df['stop'])

# Calculate session length
df['session_length'] = (df['stop'] - df['start']).dt.total_seconds()

# Group by client and calculate mean session length
mean_session_lengths = df.groupby('client_name')['session_length'].mean()

# Print results
print(mean_session_lengths)
