"""Investigation: This script investigates the patterns of daily transitions between clients over the last week and their impact on overall time allocation. By analyzing recent time-tracking data, calculating daily transitions for each client, and printing the results in a clear format, it provides insights into potential imbalances or patterns that could inform adjustments to priorities or alert thresholds.
Generated: 20260307_202058 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent entries (last 7 days)
entries = query_entries(days=7)

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate daily transitions between clients
daily_transitions = df.groupby(['client_name', 'day_of_week'])['project_name'].count().reset_index()

# Print the results
print(daily_transitions)
