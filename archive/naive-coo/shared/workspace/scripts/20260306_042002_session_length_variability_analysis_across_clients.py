"""Investigation: This script investigates the factors contributing to the session length variability within each client, providing insights into how these factors impact overall time allocation against target priorities.
Generated: 20260306_042002 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent entries
entries = query_entries(days=14)

# Convert to DataFrame
df = entries_to_dataframe(entries)

# Group by client and calculate mean session length
mean_session_lengths = df.groupby('client_name')['duration_seconds'].mean()

# Print results
print(mean_session_lengths)
