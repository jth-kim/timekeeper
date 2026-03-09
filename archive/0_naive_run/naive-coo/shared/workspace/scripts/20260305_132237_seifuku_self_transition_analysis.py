"""Investigation: This script investigates the factors contributing to the high self-transition rate of SEIFUKU and its impact on overall time allocation against target priorities. It calculates the self-transition rate, average session length, and total time spent on SEIFUKU, providing insights into potential imbalances or patterns that could inform adjustments to alert thresholds configuration.
Generated: 20260305_132237 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent entries
entries = query_entries(days=14)

# Convert to DataFrame
df = entries_to_dataframe(entries)

# Filter SEIFUKU entries
seifuku_df = df[df['client_name'] == 'SEIFUKU']

# Calculate self-transition rate
self_transition_rate = (seifuku_df['project_name'] == seifuku_df['project_name'].shift(1)).mean()

# Print findings
print(f'SEIFUKU self-transition rate: {self_transition_rate:.2f}')

# Investigate factors contributing to high self-transition rate
if self_transition_rate > 0.5:
    print('High self-transition rate detected. Investigating further...')
    # Calculate average session length for SEIFUKU
    avg_session_length = seifuku_df['duration_seconds'].mean()
    print(f'Average SEIFUKU session length: {avg_session_length:.2f} seconds')
    
    # Calculate total time spent on SEIFUKU
    total_time_spent = seifuku_df['duration_seconds'].sum()
    print(f'Total time spent on SEIFUKU: {total_time_spent:.2f} seconds')
else:
    print('Self-transition rate within normal range.')
