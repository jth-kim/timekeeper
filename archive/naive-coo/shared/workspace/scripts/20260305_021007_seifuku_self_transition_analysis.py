"""Investigation: This script investigates the factors contributing to the high self-transition rate of SEIFUKU and its impact on overall time allocation against target priorities. It calculates the self-transition rate, analyzes the time allocation, and calculates the deviation from target priorities.
Generated: 20260305_021007 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query entries for the last 30 days
entries = query_entries(days=30)

# Convert to dataframe
df = pd.DataFrame(entries)

# Filter for SEIFUKU entries
seifuku_df = df[df['client_name'] == 'SEIFUKU']

# Calculate self-transition rate
self_transition_rate = (seifuku_df['project_name'] == seifuku_df['project_name'].shift(1)).mean()

# Print result
print(f'SEIFUKU self-transition rate: {self_transition_rate}')

# Analyze impact on time allocation
time_allocation = df.groupby('client_name')['duration'].sum()
print(time_allocation)

# Calculate deviation from target priorities
target_priorities = {'STAR': 0.55, 'BBOY': 0.2, 'SEIFUKU': 0.15, 'BOJ': 0.1}
actual_allocation = time_allocation / time_allocation.sum()
deviation = (actual_allocation - pd.Series(target_priorities)).abs()
print(deviation)
