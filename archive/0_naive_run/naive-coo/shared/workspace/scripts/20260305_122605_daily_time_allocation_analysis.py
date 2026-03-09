"""Investigation: This script investigates the daily time allocation patterns across different clients over the last week and compares these patterns to the target allocations, providing insights into potential imbalances or deviations from long-term goals.
Generated: 20260305_122605 UTC
"""


import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds

# Query recent entries (last 7 days)
entries = query_entries(days=7)

# Convert entries to a DataFrame with proper types
df = pd.DataFrame(entries)

# Calculate daily time allocation for each client
daily_allocations = df.groupby('client_name')['duration'].apply(lambda x: x.apply(parse_duration_seconds).sum()).reset_index()

# Print daily allocations in a clear format
print(daily_allocations)
