"""Investigation: This script calculates the actual hour totals for each client over the last week and compares these totals to the target allocations, providing insights into potential imbalances in time allocation.
Generated: 20260306_072941 UTC
"""


import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds

# Query recent entries (last week)
entries = query_entries(days=7)

# Convert entries to a DataFrame with proper types
df = pd.DataFrame(entries)

# Calculate total hours for each client
client_hours = df.groupby('client_name')['duration'].apply(lambda x: sum(parse_duration_seconds(d) / 3600 for d in x)).reset_index()

# Print the results
print(client_hours)
