"""Investigation: This script investigates the factors contributing to the variability in untracked time between sessions and assesses their impact on overall time allocation against target priorities. By analyzing recent time-tracking data, it calculates average untracked times for each client and provides statistics on total untracked time.
Generated: 20260305_044204 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query recent entries for analysis
entries = query_entries(days=14)

# Convert to dataframe
df = pd.DataFrame(entries)

# Ensure 'start' column is datetime for calculations
df['start'] = pd.to_datetime(df['start'])

# Calculate untracked time between sessions
df['untracked_time'] = (df['start'].shift(-1) - df['stop']).abs()

# Group by client and calculate average untracked time
avg_untracked_time_by_client = df.groupby('client_name')['untracked_time'].mean()

# Print findings
print('Average untracked time by client:')
print(avg_untracked_time_by_client)

# Calculate total untracked time across all clients
total_untracked_time = df['untracked_time'].sum()

# Print total untracked time
print(f'Total untracked time: {total_untracked_time} seconds')
