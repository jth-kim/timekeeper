"""Investigation: This script analyzes the distribution of session lengths across different days of the week for SEIFUKU and compares it to the overall target allocations. It helps understand if there are specific days when SEIFUKU sessions are longer or shorter, which could inform adjustments to the time allocation strategy to better align with long-term goals.
Generated: 20260305_044740 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query entries for the last 30 days
entries = query_entries(days=30)

# Convert to dataframe
df = pd.DataFrame(entries)

# Filter for SEIFUKU entries
seifuku_df = df[df['client_name'] == 'SEIFUKU']

# Calculate session length in seconds
seifuku_df['session_length_seconds'] = seifuku_df['duration'].apply(lambda x: int(x.total_seconds()))

# Group by day of week and calculate mean session length
mean_session_lengths = seifuku_df.groupby(seifuku_df['start'].dt.dayofweek)['session_length_seconds'].mean()

# Print the distribution of session lengths across days of the week
print(mean_session_lengths)

# Compare to overall target allocations
target_allocations = {'STAR': 0.55, 'BBOY': 0.2, 'SEIFUKU': 0.15, 'BOJ': 0.1}
seifuku_target_allocation = target_allocations['SEIFUKU']

# Calculate the actual allocation for SEIFUKU based on session lengths
actual_seifuku_allocation = seifuku_df['session_length_seconds'].sum() / df['session_length_seconds'].sum()

# Print the comparison between actual and target allocations for SEIFUKU
print(f'Actual SEIFUKU allocation: {actual_seifuku_allocation:.2f}, Target allocation: {seifuku_target_allocation:.2f}')
