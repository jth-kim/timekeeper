"""Investigation: This script investigates the relationships between client transitions and session lengths across different days of the week, aiming to understand how these factors impact overall time allocation against target priorities.
Generated: 20260307_035458 UTC
"""


import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds

# Query recent entries
entries = query_entries(days=14)

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate session lengths in seconds
df['session_length_seconds'] = df['duration'].apply(parse_duration_seconds)

# Group by client and day of week, calculate mean session length
mean_session_lengths = df.groupby(['client_name', pd.Grouper(key='start', freq='D')])['session_length_seconds'].mean().reset_index()

# Pivot for easier comparison
pivoted_df = mean_session_lengths.pivot(index='client_name', columns='start', values='session_length_seconds')

# Print the pivoted DataFrame
print(pivoted_df)
