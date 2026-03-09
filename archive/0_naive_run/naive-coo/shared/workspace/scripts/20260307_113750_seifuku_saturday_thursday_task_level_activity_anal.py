"""Investigation: This script investigates task-level activity patterns within SEIFUKU on Saturdays and Thursdays, aiming to understand how these patterns impact overall time allocation against target priorities. By analyzing recent time-tracking data, calculating mean session lengths for each day of the week, and plotting task durations, it provides insights into potential imbalances or patterns that could inform adjustments to alert thresholds configuration.
Generated: 20260307_113750 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent entries for SEIFUKU on Saturdays and Thursdays
entries = query_entries(days=14)
seifuku_entries = [entry for entry in entries if entry['client_name'] == 'SEIFUKU']
saturday_thursday_entries = [entry for entry in seifuku_entries if (pd.to_datetime(entry['start']).dayofweek == 5) or (pd.to_datetime(entry['start']).dayofweek == 3)]

# Convert to DataFrame
df = entries_to_dataframe(saturday_thursday_entries)

# Calculate mean session length and duration for each day of the week
mean_session_length = df.groupby(df['start'].dt.dayofweek)['duration_seconds'].mean()
print(mean_session_length)

# Plot bar chart of task durations
import matplotlib.pyplot as plt
task_durations = df['duration_seconds']
plt.bar(range(len(task_durations)), task_durations)
plt.xlabel('Task Index')
plt.ylabel('Duration (seconds)')
plt.title('Task Durations within SEIFUKU on Saturdays and Thursdays')
plt.savefig('/data/workspace/results/seifuku_saturday_thursday_task_durations.png')

# Investigate the relationship between session length and day of the week
session_length_by_day = df.groupby(df['start'].dt.dayofweek)['duration_seconds'].sum()
print(session_length_by_day)
