"""Investigation: This script investigates task-level activities within each client that contribute to session length variability across different days of the week. It calculates mean session lengths for each client by day and examines task descriptions to understand this variability, providing insights into potential imbalances or patterns in time allocation.
Generated: 20260307_074041 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data for all clients over the last week
entries = query_entries(days=7)

# Convert entries to a DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate session lengths in seconds and convert to minutes
df['session_length_minutes'] = df['duration_seconds'] / 60

# Group by client name and day of the week, then calculate mean session length
mean_session_lengths = df.groupby(['client_name', 'day_of_week'])['session_length_minutes'].mean().reset_index()

# Print the results in a clear format
print(mean_session_lengths)

# Further analysis: examine task descriptions for each client on different days to understand variability
for client in df['client_name'].unique():
    client_df = df[df['client_name'] == client]
    print(f'Task-level activities for {client}:')
    for day in client_df['day_of_week'].unique():
        day_df = client_df[client_df['day_of_week'] == day]
        print(f'  - On {day}s: {day_df[