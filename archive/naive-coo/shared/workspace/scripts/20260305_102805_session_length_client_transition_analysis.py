"""Investigation: This script investigates the relationship between session lengths and client transitions over the last week, providing insights into how time allocation varies across different clients and projects.
Generated: 20260305_102805 UTC
"""


import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds

# Query recent entries
entries = query_entries(days=7)

# Convert to DataFrame with proper types
df = pd.DataFrame(entries)
df['duration_seconds'] = df['duration'].apply(parse_duration_seconds)

# Calculate mean session length for each client
mean_session_lengths = df.groupby('client_name')['duration_seconds'].mean()

# Analyze transitions
transitions = df[['client_name', 'project_name']].shift() + '->' + df[['client_name', 'project_name']]
transition_counts = transitions.value_counts()

# Print findings
print('Mean session lengths by client:')
print(mean_session_lengths)
print('\
Transition counts:')
print(transition_counts)
