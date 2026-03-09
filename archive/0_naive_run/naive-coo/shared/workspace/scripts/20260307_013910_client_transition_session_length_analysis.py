"""Investigation: This script investigates the relationship between client transitions and session lengths, aiming to understand how these transitions impact overall time allocation against target priorities. By analyzing recent time-tracking data and calculating mean session lengths for each client transition, it provides insights into potential imbalances or patterns that could inform adjustments to alert thresholds configuration.
Generated: 20260307_013910 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data
entries = query_entries(days=14)

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate session lengths and client transitions
df['session_length'] = df['duration_seconds']
df['client_transition'] = df['client_name'].shift(1) != df['client_name']

# Group by client transition and calculate mean session length
transition_session_lengths = df.groupby('client_transition')['session_length'].mean()

# Print results
print(transition_session_lengths)
