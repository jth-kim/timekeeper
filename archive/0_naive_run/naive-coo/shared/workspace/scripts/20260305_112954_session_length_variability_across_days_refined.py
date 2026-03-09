"""Investigation: This script investigates the patterns of session length variability across different days of the week for each client over the last 30 days. It calculates the mean session length for each client on each day of the week and prints the results in a clear, readable format.
Generated: 20260305_112954 UTC
"""


import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds

# Query recent time-tracking data
entries = query_entries(days=30)

# Convert durations to numeric values (seconds)
for entry in entries:
    entry['duration_seconds'] = parse_duration_seconds(entry['duration'])

# Create a pandas dataframe from the entries
df = pd.DataFrame(entries)

# Group by client and day of week, calculate mean session length
grouped_df = df.groupby(['client_name', df['start'].dt.dayofweek]).agg({'duration_seconds': 'mean'})

# Print the result in a clear format
print(grouped_df)