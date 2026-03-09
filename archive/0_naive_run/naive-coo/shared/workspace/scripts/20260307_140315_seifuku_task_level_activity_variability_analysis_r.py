"""Investigation: This script investigates the task-level activities within SEIFUKU that contribute to its variable session lengths across different days of the week. By analyzing recent time-tracking data and calculating mean session lengths for each day of the week, it provides insights into potential imbalances or patterns in time allocation.
Generated: 20260307_140315 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent entries for SEIFUKU
entries = query_entries(days=14, client='SEIFUKU')

# Convert to DataFrame
df = entries_to_dataframe(entries)

# Calculate session lengths and group by day of week
session_lengths = df['duration_seconds'] / 3600  # convert seconds to hours
df['day_of_week'] = pd.to_datetime(df['start']).dt.day_name()

# Group by day of week and calculate mean session length
mean_session_lengths = session_lengths.groupby(df['day_of_week']).mean()

# Print results
print(mean_session_lengths)
