"""Investigation: This script investigates the relationship between client transition patterns and session length variability across different days of the week, aiming to understand how these patterns impact overall productivity and goal alignment.
Generated: 20260307_071001 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data for the last 14 days
entries = query_entries(days=14)

# Convert entries to a DataFrame with proper types
df = entries_to_dataframe(entries)

# Ensure 'start' and 'stop' columns are datetime
df['start'] = pd.to_datetime(df['start'])
df['stop'] = pd.to_datetime(df['stop'])

# Calculate session length in seconds
df['session_length_seconds'] = (df['stop'] - df['start']).dt.total_seconds()

# Group by client name and day of week, calculate mean session length
grouped_df = df.groupby([pd.Grouper(key='start', freq='D'), 'client_name'])['session_length_seconds'].mean().reset_index()

# Pivot the DataFrame for easier comparison
pivoted_df = grouped_df.pivot(index='start', columns='client_name', values='session_length_seconds')

# Print the pivoted DataFrame
print(pivoted_df)
