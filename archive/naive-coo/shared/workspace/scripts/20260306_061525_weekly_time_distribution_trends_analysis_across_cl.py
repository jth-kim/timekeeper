"""Investigation: This script investigates the weekly time distribution trends across clients over the last 30 days, providing insights into how time allocation varies by client and week. By calculating the total time spent on each client per week and pivoting the dataframe for easier comparison, this analysis assesses whether the current allocation aligns with target priorities.
Generated: 20260306_061525 UTC
"""


from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data
entries = query_entries(days=30)

# Convert entries to a DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate total time spent on each client per week
weekly_time_df = df.groupby([pd.Grouper(key='start', freq='W'), 'client_name'])['duration_seconds'].sum().reset_index()

# Pivot the dataframe for easier comparison
pivoted_df = weekly_time_df.pivot(index='start', columns='client_name', values='duration_seconds')

# Calculate the percentage of total time spent on each client per week
percentage_df = pivoted_df.div(pivoted_df.sum(axis=1), axis=0) * 100

# Print the results in a clear format
print(percentage_df)
