"""Investigation: This script investigates the factors contributing to the variability in untracked time between sessions and assesses their impact on overall time allocation against target priorities. It adjusts the dataframe to ensure the 'start' column is of the correct data type for analysis, calculates untracked time between sessions, and provides statistics on average untracked time by client.
Generated: 20260305_022425 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query entries for the last 14 days
entries = query_entries(days=14)

# Convert to dataframe
df = pd.DataFrame(entries)

# Ensure 'start' column is datetime
df['start'] = pd.to_datetime(df['start'])

# Sort by start time
df.sort_values(by='start', inplace=True)

# Calculate untracked time between sessions
df['untracked_time'] = df['start'].diff().dt.total_seconds()

# Remove first row (no previous session)
df = df.iloc[1:]

# Group by client and calculate average untracked time
avg_untracked_time = df.groupby('client_name')['untracked_time'].mean()

# Print results
print(avg_untracked_time)
