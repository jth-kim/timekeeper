"""Investigation: This script investigates the temporal patterns of gaps between sessions across different days of the week for each client, providing insights into how these patterns impact overall time allocation against target priorities.
Generated: 20260307_235751 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query recent entries
entries = query_entries(days=14)

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Ensure 'start' column is datetime for analysis
df['start'] = pd.to_datetime(df['start'])

# Sort by start time to analyze gaps
df.sort_values(by='start', inplace=True)

# Calculate gaps between sessions in seconds
gaps = []
for i in range(1, len(df)):
    gap = (df.iloc[i]['start'] - df.iloc[i-1]['stop']).total_seconds()
    gaps.append(gap)

# Add gaps to the DataFrame
df['gap'] = [None] + gaps

# Group by client and day of week, calculate mean gap length
mean_gaps = df.groupby(['client_name', df['start'].dt.dayofweek])['gap'].mean().reset_index()

# Print results in a clear format
print(mean_gaps)