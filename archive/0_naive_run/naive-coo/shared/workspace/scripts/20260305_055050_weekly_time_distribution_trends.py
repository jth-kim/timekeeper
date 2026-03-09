"""Investigation: This script investigates the trends in weekly time distribution across clients over the last 30 days and compares these trends to the overall time allocation targets. The goal is to understand how time allocation varies by client and week, and whether these variations align with long-term goals.
Generated: 20260305_055050 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query time-tracking data for the last 30 days
entries = query_entries(days=30)

# Convert entries to a pandas DataFrame
df = pd.DataFrame(entries)

# Calculate weekly time distribution for each client
weekly_time_df = df.groupby([pd.Grouper(key='start', freq='W'), 'client_name'])['duration'].sum().reset_index()

# Calculate overall time allocation targets
target_allocations = {
    'STAR': 0.55,
    'BBOY': 0.2,
    'SEIFUKU': 0.15,
    'BOJ': 0.1
}

# Compare weekly time distribution trends to overall time allocation targets
comparison_df = weekly_time_df.merge(pd.DataFrame(list(target_allocations.items()), columns=['client_name', 'target_allocation']), on='client_name')

# Print findings
print(comparison_df)
