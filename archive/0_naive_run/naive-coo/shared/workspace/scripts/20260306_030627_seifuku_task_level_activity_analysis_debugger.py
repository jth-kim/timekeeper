"""Investigation: This script investigates the root causes of the empty Series returned by the 'seifuku_task_level_activity_analysis_refined' script and proposes modifications to the data collection or processing pipeline to prevent such errors in the future.
Generated: 20260306_030627 UTC
"""


from supabase_helper import query_entries, parse_duration_seconds, entries_to_dataframe
import pandas as pd

# Query recent entries for SEIFUKU
entries = query_entries(days=30)
seifuku_entries = [entry for entry in entries if entry['client_name'] == 'SEIFUKU']

# Convert to DataFrame
df = entries_to_dataframe(seifuku_entries)

# Check for missing values in 'description' column
missing_descriptions = df[df['description'].isnull()]
print('Missing descriptions:', missing_descriptions.shape[0])

# Investigate task-level activities within SEIFUKU
task_durations = df.groupby('description')['duration_seconds'].mean()
print(task_durations)

# Identify potential issues with data processing
if 'description' not in df.columns:
    print('Description column is missing')
elif df['description'].isnull().any():
    print('Null values found in description column')

# Compute total time spent on SEIFUKU tasks
total_time_seifuku = df['duration_seconds'].sum()
print(f'Total time spent on SEIFUKU tasks: {total_time_seifuku} seconds')
