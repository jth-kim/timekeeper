"""Investigation: This script investigates client-specific time allocation trends over the last 14 days and compares these trends to the target allocations. It calculates the total time spent on each client and prints the results, providing insights into potential imbalances in time allocation.
Generated: 20260306_200821 UTC
"""


import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds

# Query entries for the last 14 days
entries = query_entries(days=14)

# Convert entries to a DataFrame
df = pd.DataFrame(entries)

# Calculate total time spent on each client
client_time_allocations = df.groupby('client_name')['duration'].apply(lambda x: sum(parse_duration_seconds(d) for d in x))

# Print client-specific time allocation trends
print(client_time_allocations)
