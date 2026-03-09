"""Investigation: This script investigates the relationship between session lengths and client transitions by analyzing recent time-tracking data. It calculates the average session length for each client after a project transition, providing insight into how time allocation varies across different clients and projects.
Generated: 20260305_164324 UTC
"""

import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds

df = entries_to_dataframe(query_entries(days=14))
# Calculate session length in seconds for each entry and add it to the dataframe
df['session_length'] = df['duration'].apply(parse_duration_seconds)

clients = df['client_name'].unique()
for client in clients:
    client_df = df[df['client_name'] == client]
    transitions = client_df['project_name'].shift() != client_df['project_name']
    transition_session_lengths = client_df[transitions]['session_length']
    if not transition_session_lengths.empty:
        print(f'Client: {client}, Average session length after transition: {transition_session_lengths.mean()}')
    else:
        print(f'Client: {client}, No transitions found.')