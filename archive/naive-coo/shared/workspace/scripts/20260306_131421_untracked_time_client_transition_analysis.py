"""Investigation: This script investigates the gaps between sessions (untracked time) for each client over the last week, aiming to understand how these gaps impact overall time allocation. By calculating the mean untracked time for each client, it provides insights into potential imbalances or patterns that could inform adjustments to alert thresholds configuration.
Generated: 20260306_131421 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query recent entries
entries = query_entries(days=7)

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate session start and stop times
df['start'] = pd.to_datetime(df['start'])
df['stop'] = pd.to_datetime(df['stop'])

# Sort by start time
df = df.sort_values('start')

# Initialize list for untracked times
untracked_times = []

# Iterate through sessions to calculate gaps (untracked time)
for i in range(1, len(df)):
    previous_stop = df.iloc[i-1]['stop']
    current_start = df.iloc[i]['start']
    gap = current_start - previous_stop
    untracked_times.append((df.iloc[i]['client_name'], gap.total_seconds()))

# Convert to DataFrame for easier analysis
untracked_df = pd.DataFrame(untracked_times, columns=['client', 'untracked_time'])

# Group by client and calculate mean untracked time
mean_untracked_times = untracked_df.groupby('client')['untracked_time'].mean()

print(mean_untracked_times)
