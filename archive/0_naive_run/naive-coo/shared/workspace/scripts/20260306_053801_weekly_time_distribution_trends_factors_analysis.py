"""Investigation: This script investigates the weekly time distribution trends across clients over the last 30 days and calculates the factors contributing to variability in these trends, providing insights into potential imbalances or patterns that could inform adjustments to priorities or alert thresholds.
Generated: 20260306_053801 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data for the last 30 days
recent_entries = query_entries(days=30)

# Convert to DataFrame with proper types
df = entries_to_dataframe(recent_entries)

# Calculate weekly time distribution trends across clients
weekly_trends = df.groupby('client_name')['duration_seconds'].sum().reset_index()

# Pivot dataframe for easier comparison
pivoted_df = pd.pivot_table(df, index='client_name', columns='week', values='duration_seconds')

# Calculate percentage of total time spent on each client per week
percentage_df = pivoted_df.div(pivoted_df.sum(axis=0), axis=1) * 100

# Print the results in a clear format
print('Weekly Time Distribution Trends:')
print(weekly_trends)
print('\
Percentage of Total Time Spent on Each Client Per Week:')
print(percentage_df)

# Calculate factors contributing to variability in weekly time distribution trends
factors = []
for client in df['client_name'].unique():
    client_df = df[df['client_name'] == client]
    avg_session_length = client_df['duration_seconds'].mean()
    std_dev_session_length = client_df['duration_seconds'].std()
    factors.append({
        'client': client,
        'avg_session_length': avg_session_length,
        'std_dev_session_length': std_dev_session_length
    })

# Print the factors contributing to variability in weekly time distribution trends
print('\
Factors Contributing to Variability in Weekly Time Distribution Trends:')
for factor in factors:
    print(f'Client: {factor[