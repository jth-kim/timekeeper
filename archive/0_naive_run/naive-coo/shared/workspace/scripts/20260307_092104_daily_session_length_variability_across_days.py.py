"""Investigation: This script calculates the daily session length variability across different days of the week for each client, providing insights into how productivity varies and whether there are patterns that could inform adjustments to priorities or alert thresholds.
Generated: 20260307_092104 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Get recent entries
entries = query_entries(days=14)

# Convert to DataFrame
df = entries_to_dataframe(entries)

# Ensure 'start' is datetime for grouping by day of week
df['start'] = pd.to_datetime(df['start'])

# Group by client and day of week, calculate mean session length
daily_session_lengths = df.groupby([pd.Grouper(key='start', freq='D'), 'client_name'])['duration_seconds'].mean().reset_index()

# Pivot for easier comparison across days
pivoted_df = daily_session_lengths.pivot(index='client_name', columns='start', values='duration_seconds')

# Calculate standard deviation of session lengths by day for each client
std_dev_by_day = pivoted_df.std(axis=1)

# Print results
print(std_dev_by_day)
