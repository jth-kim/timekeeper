"""Investigation: This script investigates the factors contributing to the high average session duration for SEIFUKU tasks and assesses their impact on overall time allocation against target priorities. It calculates the average session duration for each task within SEIFUKU, identifies top tasks contributing to this duration, and evaluates the percentage of total time allocated to SEIFUKU tasks.
Generated: 20260307_001016 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent entries for SEIFUKU client
entries = query_entries(days=14, client_name='SEIFUKU')

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate average session duration for each task within SEIFUKU
average_durations = df.groupby('description')['duration_seconds'].mean().sort_values(ascending=False)

# Print top tasks contributing to high average session duration
print('Top tasks contributing to high average session duration for SEIFUKU:')
print(average_durations.head(5))

# Investigate the impact on overall time allocation
total_seifuku_time = df['duration_seconds'].sum()
total_time = query_entries(days=14)
total_time_df = entries_to_dataframe(total_time)
total_time_spent = total_time_df['duration_seconds'].sum()

print(f'Total time spent on SEIFUKU: {total_seifuku_time / 3600} hours')
print(f'Total time spent across all clients: {total_time_spent / 3600} hours')

# Calculate percentage of total time allocated to SEIFUKU
seifuku_percentage = (total_seifuku_time / total_time_spent) * 100

print(f'SEIFUKU tasks account for {seifuku_percentage:.2f}% of total time allocation')
