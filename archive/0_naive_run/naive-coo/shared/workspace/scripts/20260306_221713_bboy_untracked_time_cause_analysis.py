"""Investigation: This script investigates the factors contributing to the high untracked time for BBOY and assesses their impact on overall productivity. It queries recent time-tracking data, filters for BBOY entries, calculates total untracked time, and identifies specific sessions with unusually high untracked times.
Generated: 20260306_221713 UTC
"""


from supabase_helper import query_entries, parse_duration_seconds, entries_to_dataframe

# Query recent entries
entries = query_entries(days=14)

# Convert to DataFrame with proper duration handling
df = entries_to_dataframe(entries)

# Filter for BBOY entries
df_bboy = df[df['client_name'] == 'BBOY']

# Calculate total untracked time for BBOY
untracked_time_bboy = df_bboy['untracked_time'].sum()

# Print findings
print(f'Total untracked time for BBOY: {untracked_time_bboy} seconds')

# Investigate factors contributing to high untracked time
factors = []
for index, row in df_bboy.iterrows():
  if row['untracked_time'] > 3600:  # More than 1 hour
    factors.append((row['start'], row['stop'], row['untracked_time']))

# Print factors
print('Factors contributing to high untracked time for BBOY:')
for factor in factors:
  print(factor)
