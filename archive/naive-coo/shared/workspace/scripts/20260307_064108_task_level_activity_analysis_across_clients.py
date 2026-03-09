"""Investigation: This script investigates task-level activities within each client that contribute to session length variability and assesses their alignment with the Sovereign's broader objectives. By analyzing recent time-tracking data, calculating mean session lengths for each client, and examining task descriptions, this script provides insights into potential imbalances or patterns in time allocation.
Generated: 20260307_064108 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

df = entries_to_dataframe(query_entries(days=14))
# Calculate session lengths in seconds
session_lengths = df['duration_seconds']

df['client_project'] = df['client_name'] + ' / ' + df['project_name']

task_level_activities = df.groupby('client_project')['description'].value_counts().reset_index(name='count')
print(task_level_activities)
