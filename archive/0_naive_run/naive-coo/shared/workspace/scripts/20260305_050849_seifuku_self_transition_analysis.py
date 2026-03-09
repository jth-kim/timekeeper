"""Investigation: This script investigates the underlying reasons for the high self-transition rate of SEIFUKU and its impact on the overall time allocation strategy. It analyzes recent entries, calculates the self-transition rate, and examines factors contributing to this rate. Additionally, it assesses the impact on time allocation by calculating the percentage of total time spent on SEIFUKU.
Generated: 20260305_050849 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query recent entries to analyze SEIFUKU sessions
entries = query_entries(days=14)

# Convert to DataFrame for easier analysis
df = pd.DataFrame(entries)

# Filter for SEIFUKU entries
seifuku_df = df[df['client_name'] == 'SEIFUKU']

# Calculate self-transition rate
self_transitions = seifuku_df['project_name'].shift() == seifuku_df['project_name']
self_transition_rate = self_transitions.mean()

print(f'SEIFUKU self-transition rate: {self_transition_rate}')

# Investigate factors contributing to high self-transition rate
factors_df = seifuku_df[self_transitions]
print('Factors contributing to high self-transition rate:')
print(factors_df.describe())

# Analyze impact on overall time allocation strategy
time_allocation_df = df.groupby('client_name')['duration'].sum().reset_index()
print('Time allocation by client:')
print(time_allocation_df)

# Calculate percentage of total time spent on SEIFUKU
seifuku_time_percentage = (time_allocation_df.loc[time_allocation_df['client_name'] == 'SEIFUKU', 'duration'].values[0] / time_allocation_df['duration'].sum()) * 100
print(f'SEIFUKU time percentage: {seifuku_time_percentage}%')
