"""Investigation: This script investigates the weekly time distribution trends across clients over the last 30 days and compares these trends to the target allocations. It calculates the total time spent on each client per week, pivots the DataFrame for easier comparison, and then calculates the percentage of total time spent on each client per week.
Generated: 20260306_004012 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent entries
entries = query_entries(days=30)

# Convert to DataFrame
df = entries_to_dataframe(entries)

# Group by client and week
weekly_df = df.groupby([pd.Grouper(key='start', freq='W'), 'client_name']).agg({'duration_seconds': 'sum'}).reset_index()

# Calculate percentage of total time spent on each client per week
weekly_df['percentage'] = weekly_df.groupby('start')['duration_seconds'].apply(lambda x: 100 * x / x.sum())

# Print the results
print(weekly_df)
