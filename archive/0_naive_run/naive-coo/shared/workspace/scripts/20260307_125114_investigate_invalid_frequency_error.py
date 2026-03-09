"""Investigation: This script investigates the technical reasons behind the invalid frequency error in the hourly_session_length_analysis script and modifies it to successfully retrieve and process data for analysis. It loads recent entries, converts them to a dataframe, groups by client and hour of day, calculates mean session lengths, and prints the results.
Generated: 20260307_125114 UTC
"""


import pandas as pd

# Load recent entries
entries = query_entries(days=7)

# Convert entries to dataframe
df = entries_to_dataframe(entries)

# Group by client and hour of day
grouped_df = df.groupby([pd.Grouper(key='start', freq='h'), 'client_name'])

# Calculate mean session length for each group
mean_session_lengths = grouped_df['duration_seconds'].mean()

# Print results
print(mean_session_lengths)
