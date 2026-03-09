"""Investigation: This script investigates the trends in weekly time distribution across clients over the last 30 days and compares these trends to the overall time allocation targets. It queries recent time-tracking data, converts it into a pandas DataFrame, ensures the 'start' column is in datetime format for grouping by week, groups the data by client and week, calculates total duration per group, and finally calculates the mean weekly duration for each client.
Generated: 20260305_062150 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query recent time-tracking data
entries = query_entries(days=30)

# Convert to DataFrame
df = pd.DataFrame(entries)

# Ensure 'start' column is datetime format for grouping by week
df['start'] = pd.to_datetime(df['start'])

# Group by client and week, calculate total duration per group
weekly_durations = df.groupby([pd.Grouper(key='start', freq='W'), 'client_name'])['duration'].sum().reset_index()

# Calculate mean weekly duration for each client
mean_weekly_durations = weekly_durations.groupby('client_name')['duration'].mean().reset_index()

# Print results
print(mean_weekly_durations)
