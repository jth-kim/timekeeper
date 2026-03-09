"""Investigation: This script investigates the underlying causes of the high variability in STAR's session lengths and how these variabilities impact the Sovereign's broader objectives. It calculates the session length variability, average session lengths for each day of the week, and total time spent on STAR over the last 14 days.
Generated: 20260307_092715 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query entries for the last 14 days
entries = query_entries(days=14)

# Convert entries to a DataFrame
df = entries_to_dataframe(entries)

# Filter for STAR entries
star_df = df[df['client_name'] == 'STAR']

# Calculate session length variability
session_length_variability = star_df['duration_seconds'].std()

# Print the result
print(f'Session length variability for STAR: {session_length_variability}')

# Investigate the underlying causes of high variability
# Calculate the average session length for each day of the week
average_session_lengths = star_df.groupby(star_df['start'].dt.dayofweek)['duration_seconds'].mean()

# Print the result
print('Average session lengths for STAR by day of week:')
print(average_session_lengths)

# Investigate the impact on broader objectives
# Calculate the total time spent on STAR over the last 14 days
total_star_time = star_df['duration_seconds'].sum()

# Print the result
print(f'Total time spent on STAR over the last 14 days: {total_star_time} seconds')
