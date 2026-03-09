"""Investigation: This script investigates the task-level activities within each client that contribute to session length variability and assesses their impact on overall time allocation against target priorities. It calculates the mean session length for each client, groups tasks by duration, and plots a bar chart of task durations.
Generated: 20260306_024541 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent entries
entries = query_entries(days=30)

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Filter for each client and calculate mean session length
clients = df['client_name'].unique()
for client in clients:
    client_df = df[df['client_name'] == client]
    mean_session_length = client_df['duration_seconds'].mean()
    print(f'Mean session length for {client}: {mean_session_length} seconds')

# Group by task and calculate mean duration
task_durations = df.groupby('description')['duration_seconds'].mean()
print(task_durations)

# Plot a bar chart of task durations
import matplotlib.pyplot as plt
task_durations.plot(kind='bar')
plt.savefig('/data/workspace/results/task_durations.png')
