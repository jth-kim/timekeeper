"""Investigation: This script investigates the patterns of session lengths for each client across different times of the day to understand how time allocation varies by hour and client. It queries recent time-tracking data, converts it to a pandas dataframe, calculates session lengths, groups by client and hour of day, and prints the mean session length for each group.
Generated: 20260305_035031 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query recent entries
entries = query_entries(days=30)

# Convert to dataframe
df = pd.DataFrame(entries)

# Ensure 'start' and 'stop' columns are datetime
df['start'] = pd.to_datetime(df['start'])
df['stop'] = pd.to_datetime(df['stop'])

# Calculate session length in seconds
df['session_length'] = (df['stop'] - df['start']).dt.total_seconds()

# Group by client and hour of day, calculate mean session length
grouped_df = df.groupby([pd.Grouper(key='start', freq='H'), 'client_name'])['session_length'].mean().reset_index()

# Print findings
print(grouped_df)
