"""Investigation: This script investigates the task-level activity patterns within SEIFUKU on Sundays, focusing on both task types and durations to understand their contribution to variable session lengths. By analyzing recent time-tracking data, calculating mean session lengths for each task-level activity, and printing the results in a clear format, it provides insights into potential imbalances or patterns that could inform adjustments to priorities or alert thresholds.
Generated: 20260307_203853 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query recent time-tracking data for SEIFUKU on Sundays
sunday_seifuku_entries = [entry for entry in query_entries(days=14) if 'Sunday' in entry['start'] and entry['client_name'] == 'SEIFUKU']

# Convert to pandas DataFrame
df = pd.DataFrame(sunday_seifuku_entries)

# Calculate session lengths in seconds
df['duration_seconds'] = df['duration'].apply(lambda x: parse_duration_seconds(x))

# Group by task-level activity (description) and calculate mean session length
mean_session_lengths = df.groupby('description')['duration_seconds'].mean()

# Print the top 3 tasks with the longest mean session lengths
print(mean_session_lengths.nlargest(3))
