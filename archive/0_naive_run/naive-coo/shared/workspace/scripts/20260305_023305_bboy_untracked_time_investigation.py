"""Investigation: This script investigates the underlying causes of the high untracked time for BBOY and assesses its impact on the Sovereign's overall time allocation strategy. It queries the time-tracking data for the last 14 days, filters for BBOY entries, calculates untracked time between sessions, and prints the average untracked time. If the average untracked time exceeds 1 hour, it suggests potential distractions or unnoticed patterns that may impact time allocation.
Generated: 20260305_023305 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query entries for the last 14 days
entries = query_entries(days=14)

# Convert to pandas dataframe
df = pd.DataFrame(entries)

# Filter for BBOY entries
bboy_df = df[df['client_name'] == 'BBOY']

# Calculate untracked time between sessions
untracked_time = []
for i in range(len(bboy_df) - 1):
    start_time = bboy_df.iloc[i]['stop']
    next_start_time = bboy_df.iloc[i+1]['start']
    untracked_time.append((next_start_time - start_time).total_seconds())

# Calculate average untracked time
average_untracked_time = sum(untracked_time) / len(untracked_time)

# Print findings
print(f'Average untracked time for BBOY: {average_untracked_time} seconds')

# Investigate potential causes of high untracked time
if average_untracked_time > 3600:  # 1 hour
    print('High untracked time for BBOY may indicate potential distractions or unnoticed patterns.')
else:
    print('Untracked time for BBOY appears to be within normal ranges.')
