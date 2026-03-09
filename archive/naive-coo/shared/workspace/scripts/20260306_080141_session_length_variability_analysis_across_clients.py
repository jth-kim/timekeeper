"""Investigation: This script investigates the primary factors contributing to session length variability across clients, such as task type, time of day, or day of week, and assesses their impact on overall time allocation against target priorities.
Generated: 20260306_080141 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data
entries = query_entries(days=30)

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Group by client and calculate mean session length
mean_session_lengths = df.groupby('client_name')['duration_seconds'].mean()

# Print results
print(mean_session_lengths)
