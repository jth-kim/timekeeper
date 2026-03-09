"""Investigation: This script investigates the distribution of gaps between sessions (untracked time) over the last week, providing insight into potential distractions or unnoticed patterns in the Sovereign's time allocation.
Generated: 20260304_225444 UTC
"""


import pandas as pd
from supabase_helper import query_entries, read_memory

# Query entries for the last week
entries = query_entries(days=7)

# Convert to dataframe
df = pd.DataFrame(entries)

# Calculate gaps between sessions (untracked time)
df['stop'] = pd.to_datetime(df['stop'])
df['start'] = pd.to_datetime(df['start'])
df['next_start'] = df['start'].shift(-1)
df['gap'] = (df['next_start'] - df['stop']).dt.total_seconds() / 60

# Remove last row which has no next session
df = df.iloc[:-1]

# Group gaps by day and calculate total untracked time per day
daily_gaps = df.groupby(df['stop'].dt.date)['gap'].sum().reset_index()

# Print results
print(daily_gaps)
