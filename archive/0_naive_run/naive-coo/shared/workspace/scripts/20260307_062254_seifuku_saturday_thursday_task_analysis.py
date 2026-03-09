"""Investigation: This script investigates the task-level activities within SEIFUKU that contribute to its longer session lengths on Saturdays and Thursdays, aiming to understand how these activities align with the Sovereign's broader objectives.
Generated: 20260307_062254 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data for SEIFUKU on Saturdays and Thursdays
entries = query_entries(days=14)
seifuku_entries = [entry for entry in entries if entry['client_name'] == 'SEIFUKU']

# Filter entries by day of week (Saturday or Thursday)
saturday_thursday_entries = []
for entry in seifuku_entries:
    start_time = pd.to_datetime(entry['start'])
    if start_time.dayofweek in [5, 3]:  # 5: Saturday, 3: Thursday
        saturday_thursday_entries.append(entry)

# Convert entries to a pandas DataFrame with proper types
df = entries_to_dataframe(saturday_thursday_entries)

# Calculate mean session length for each task within SEIFUKU on Saturdays and Thursdays
mean_session_lengths = df.groupby('description')['duration_seconds'].mean()

# Print the results in a clear format
print(mean_session_lengths)
