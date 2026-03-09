"""Investigation: This script investigates the relationship between client transitions and session lengths, aiming to understand how these transitions impact overall time allocation against target priorities. By analyzing recent time-tracking data and calculating mean session lengths for each client transition, it provides insights into potential imbalances or patterns that could inform adjustments to alert thresholds configuration.
Generated: 20260307_005737 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data
entries = query_entries(days=14)

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate session length in seconds
df['session_length'] = df['duration_seconds']

# Group by client transition and calculate mean session length
client_transitions = df.groupby(['client_name', 'project_name'])['session_length'].mean().reset_index()

# Print results
print(client_transitions)
