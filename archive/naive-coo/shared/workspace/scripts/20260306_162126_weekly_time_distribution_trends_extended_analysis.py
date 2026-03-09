"""Investigation: This script investigates weekly time distribution trends across clients over an extended period and compares these trends to target allocations, providing insights into potential imbalances or patterns in time allocation.
Generated: 20260306_162126 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data for 90 days
entries = query_entries(days=90)

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Ensure 'start' column is datetime for grouping by week
df['start'] = pd.to_datetime(df['start'])

# Group by client and week, summing duration_seconds
weekly_totals = df.groupby([pd.Grouper(key='start', freq='W'), 'client_name'])['duration_seconds'].sum().reset_index()

# Pivot for easier comparison across weeks and clients
pivoted_df = weekly_totals.pivot(index='start', columns='client_name', values='duration_seconds')

# Calculate percentage of total time spent on each client per week
total_time_per_week = pivoted_df.sum(axis=1)
percentage_per_client = (pivoted_df.div(total_time_per_week, axis=0) * 100).round(2)

# Print the resulting DataFrame for inspection
print(percentage_per_client)
