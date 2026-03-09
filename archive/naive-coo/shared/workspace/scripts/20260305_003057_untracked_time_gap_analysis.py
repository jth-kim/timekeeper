"""Investigation: This script investigates the factors contributing to the significant gaps between logged sessions (untracked time) and assesses their impact on overall time allocation against target priorities. It calculates the average gap size and total untracked time over the last 14 days, providing insights into potential distractions or unnoticed patterns in the Sovereign's time allocation.
Generated: 20260305_003057 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query recent entries
entries = query_entries(days=14)

# Convert to dataframe
df = pd.DataFrame(entries)

# Ensure 'start' column is datetime
df['start'] = pd.to_datetime(df['start'])

# Calculate time differences between sessions
df['time_diff'] = df['start'].diff()

# Convert time differences to seconds
df['time_diff_seconds'] = df['time_diff'].dt.total_seconds()

# Filter out rows with missing values (first row will have NaN)
df_filtered = df.dropna(subset=['time_diff_seconds'])

# Calculate average gap size
average_gap_size = df_filtered['time_diff_seconds'].mean()

# Print findings
print(f'Average gap size between logged sessions: {average_gap_size} seconds')

# Assess impact on time allocation
total_untracked_time = df_filtered['time_diff_seconds'].sum()
print(f'Total untracked time in the last 14 days: {total_untracked_time} seconds')
