"""Investigation: This script investigates the task-level activities within each client that contribute to the observed session length patterns by day of the week, aiming to understand how these activities impact overall productivity. By analyzing recent time-tracking data and calculating mean session lengths for each client by day of the week, it provides insights into potential imbalances or patterns in time allocation.
Generated: 20260306_211540 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data for the last 14 days
entries = query_entries(days=14)

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Group by client and day of week, then calculate mean session length
grouped_df = df.groupby(['client_name', pd.Grouper(key='start', freq='W-MON')])['duration_seconds'].mean().reset_index()

# Print the results in a clear format
print(grouped_df)
