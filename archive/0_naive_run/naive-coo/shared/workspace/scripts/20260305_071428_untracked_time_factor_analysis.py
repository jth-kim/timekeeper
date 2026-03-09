"""Investigation: This script aims to investigate the factors contributing to variability in untracked time across different clients. By analyzing recent time-tracking data, converting 'start' and 'stop' columns to datetime format, calculating session lengths and untracked times, and grouping by client, it provides insights into which clients have significant untracked times and how these might affect overall time allocation against target priorities.
Generated: 20260305_071428 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query recent entries (up to 90 days back)
entries = query_entries(days=90)

# Convert the data into a DataFrame for easier manipulation
df = pd.DataFrame(entries)

# Ensure 'start' and 'stop' columns are in datetime format
df['start'] = pd.to_datetime(df['start'])
df['stop'] = pd.to_datetime(df['stop'])

# Calculate session lengths in seconds
df['session_length'] = (df['stop'] - df['start']).dt.total_seconds()

# Sort the DataFrame by 'start' time to calculate untracked times
df.sort_values(by='start', inplace=True)

# Calculate untracked time between sessions in seconds
df['untracked_time'] = (df['start'].diff()).dt.total_seconds()

# Group by client and calculate mean untracked time for each
mean_untracked_times = df.groupby('client_name')['untracked_time'].mean().reset_index()

# Print the results to understand which clients have high untracked times
print(mean_untracked_times)

# Further analysis could involve looking at specific tasks or projects within clients
# to identify patterns or causes of high untracked time, and assessing their impact on overall time allocation.
