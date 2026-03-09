"""Investigation: This script investigates the specific task-level activities within each project that contribute to the observed session length variability across clients and assesses their alignment with the Sovereign's long-term objectives.
Generated: 20260306_110715 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data
entries = query_entries(days=30)

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Filter for specific clients and projects
seifuku_df = df[df['client_name'] == 'SEIFUKU']
star_df = df[df['client_name'] == 'STAR']
bboy_df = df[df['client_name'] == 'BBOY']

# Calculate mean session length for each task within each client
seifuku_task_lengths = seifuku_df.groupby('project_name')['duration_seconds'].mean()
star_task_lengths = star_df.groupby('project_name')['duration_seconds'].mean()
bboy_task_lengths = bboy_df.groupby('project_name')['duration_seconds'].mean()

# Print results
print('SEIFUKU task lengths:')
print(seifuku_task_lengths)
print('STAR task lengths:')
print(star_task_lengths)
print('BBOY task lengths:')
print(bboy_task_lengths)

# Investigate alignment with long-term objectives
# ... (add code to analyze alignment with Sovereign's goals)
