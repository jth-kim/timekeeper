"""Investigation: This script investigates the temporal patterns of task-level activities within each client, aiming to understand how these patterns impact overall time allocation. By analyzing recent time-tracking data and calculating mean durations for each task-level activity by day of week, it provides insights into potential imbalances or patterns that could inform adjustments to priorities or alert thresholds.
Generated: 20260307_205543 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent entries
entries = query_entries(days=14)

# Convert to DataFrame
df = entries_to_dataframe(entries)

# Ensure 'start' column is datetime
df['start'] = pd.to_datetime(df['start'])

# Extract task-level activities (description) and calculate duration in seconds
df['task_level_activity'] = df['description']
df['duration_seconds'] = df['duration_hours'] * 3600 + df['duration_minutes'] * 60

# Group by client, task-level activity, and day of week; calculate mean duration
temporal_patterns = df.groupby(['client_name', 'task_level_activity', df['start'].dt.dayofweek])['duration_seconds'].mean().reset_index()

# Print temporal patterns
print(temporal_patterns)
