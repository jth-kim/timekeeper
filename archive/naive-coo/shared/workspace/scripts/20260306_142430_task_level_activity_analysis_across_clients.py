"""Investigation: This script investigates the task-level activities within each client that contribute to session length variability and assesses their alignment with the Sovereign's objectives. It calculates the mean session length for each client and prints these averages in a clear format.
Generated: 20260306_142430 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent entries for all clients
entries = query_entries(days=14)

# Convert to DataFrame
df = entries_to_dataframe(entries)

# Group by client and calculate mean session length
client_session_lengths = df.groupby('client_name')['duration_seconds'].mean()

# Print results
print(client_session_lengths)
