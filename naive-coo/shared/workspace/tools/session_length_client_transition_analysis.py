"""Investigation: This script investigates the relationship between session lengths and client transitions by first converting the 'start' and 'stop' columns to datetime format, then calculating the session length in seconds. It groups the data by client name and project name, and finally calculates the mean session length for each group.
Generated: 20260305_033824 UTC
"""

import pandas as pd
from supabase_helper import query_entries

df = pd.DataFrame(query_entries(days=30))

df['start'] = pd.to_datetime(df['start'])
df['stop'] = pd.to_datetime(df['stop'])

df['session_length'] = df['stop'] - df['start']

df['session_length_seconds'] = df['session_length'].dt.total_seconds()

client_transitions = df[['client_name', 'project_name', 'tags', 'description', 'session_length_seconds']]

client_transitions_grouped = client_transitions.groupby(['client_name', 'project_name'])['session_length_seconds'].mean().reset_index()

print(client_transitions_grouped)