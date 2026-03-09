"""Investigation: This script investigates the weekly time distribution trends across clients over an extended period of 60 days and compares these trends to the target allocations, providing a broader perspective on time allocation patterns.
Generated: 20260306_125856 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query entries for the last 60 days
entries = query_entries(days=60)

# Convert entries to a DataFrame
df = pd.DataFrame(entries)

# Ensure 'start' column is datetime
df['start'] = pd.to_datetime(df['start'])

# Calculate weekly time distribution trends
weekly_time_df = df.groupby(pd.Grouper(key='start', freq='W')).size().reset_index(name='count')

# Pivot the DataFrame for easier comparison
pivoted_df = weekly_time_df.pivot(index='start', columns='client_name', values='count')

# Calculate the percentage of total time spent on each client per week
percentage_df = pivoted_df.div(pivoted_df.sum(axis=1), axis=0)

# Print the results
print(percentage_df)
