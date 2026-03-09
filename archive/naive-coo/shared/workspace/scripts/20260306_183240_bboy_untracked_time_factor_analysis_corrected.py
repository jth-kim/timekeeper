"""Investigation: This script investigates the factors contributing to the high untracked time for BBOY and assesses their impact on overall time allocation against target priorities. It queries recent entries for BBOY, converts them to a DataFrame, calculates the total untracked time, and prints the result.
Generated: 20260306_183240 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent entries for BBOY
bboy_entries = [entry for entry in query_entries(days=14) if entry['client_name'] == 'BBOY']

# Convert entries to DataFrame
df = entries_to_dataframe(bboy_entries)

# Calculate total untracked time for BBOY
total_untracked_time = df['untracked_time'].sum()

# Print the result
print(f'Total untracked time for BBOY: {total_untracked_time} seconds')
