"""Investigation: This script investigates the factors contributing to the high untracked time for BBOY and assesses their impact on overall time allocation against target priorities. It calculates the mean untracked time for BBOY by analyzing gaps between sessions over the last 14 days.
Generated: 20260305_102309 UTC
"""


from supabase_helper import query_entries, parse_duration_seconds
import pandas as pd

# Query recent entries to analyze gaps (untracked time) between sessions
recent_entries = query_entries(days=14)

# Convert the list of entries into a DataFrame for easier analysis
df = pd.DataFrame(recent_entries)

# Ensure 'start' and 'stop' columns are datetime format
df['start'] = pd.to_datetime(df['start'])
df['stop'] = pd.to_datetime(df['stop'])

# Calculate session duration in seconds (already numeric in this case)
df['duration_seconds'] = df.apply(lambda row: (row['stop'] - row['start']).total_seconds(), axis=1)

# Sort entries by start time to analyze gaps
df.sort_values(by='start', inplace=True)

# Initialize list to hold untracked times
untracked_times = []

# Iterate over sorted entries to calculate gaps
for i in range(1, len(df)):
    gap = (df.iloc[i]['start'] - df.iloc[i-1]['stop']).total_seconds()
    if gap > 0:  # Only consider positive gaps (i.e., actual untracked time)
        untracked_times.append(gap)

# Calculate statistics on untracked times for BBOY specifically
bboy_untracked_times = [time for time in untracked_times if df.iloc[[i for i, x in enumerate(untracked_times) if x == time][0]-1]['client_name'] == 'BBOY']

if bboy_untracked_times:
    mean_bboy_untracked_time = sum(bboy_untracked_times) / len(bboy_untracked_times)
    print(f'Mean untracked time for BBOY: {mean_bboy_untracked_time} seconds')
else:
    print('No untracked times found for BBOY.')
