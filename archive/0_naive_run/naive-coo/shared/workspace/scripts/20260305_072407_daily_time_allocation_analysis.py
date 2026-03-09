"""Investigation: This script investigates the daily time allocation patterns across different clients over the last week and compares these patterns to the overall time allocation targets. By analyzing recent time-tracking data and calculating the daily percentage allocation for each client, it provides insights into how time allocation varies by day and client, helping to identify potential imbalances or trends that could inform adjustments to achieve a more balanced time allocation.
Generated: 20260305_072407 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query entries for the last week
entries = query_entries(days=7)

# Convert to DataFrame
df = pd.DataFrame(entries)

# Ensure 'start' column is datetime format
df['start'] = pd.to_datetime(df['start'])

# Calculate daily time allocation for each client
daily_allocation = df.groupby([pd.Grouper(key='start', freq='D'), 'client_name'])['duration'].sum().reset_index()

# Pivot to get clients as columns
daily_allocation_pivot = daily_allocation.pivot(index='start', columns='client_name', values='duration')

# Calculate total daily duration
total_daily_duration = daily_allocation_pivot.sum(axis=1)

# Normalize by total daily duration to get percentage allocation
normalized_daily_allocation = daily_allocation_pivot.div(total_daily_duration, axis=0) * 100

# Print the normalized daily allocation
print(normalized_daily_allocation)
