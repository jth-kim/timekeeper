"""Investigation: This script investigates the factors contributing to the high variability in session lengths across different days of the week for SEIFUKU and assesses their impact on overall time allocation against target priorities. It calculates the standard deviation of session lengths for each day of the week and prints the results.
Generated: 20260307_105802 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent entries
entries = query_entries(days=14)

# Convert to DataFrame
df = entries_to_dataframe(entries)

# Filter for SEIFUKU
seifuku_df = df[df['client_name'] == 'SEIFUKU']

# Calculate session length variability by day of week
session_length_variability = seifuku_df.groupby(seifuku_df['start'].dt.dayofweek)['duration_seconds'].std()

# Print results
print(session_length_variability)
