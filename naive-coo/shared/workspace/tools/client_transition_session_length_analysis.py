"""Investigation: This script investigates the relationship between client transitions and session lengths, aiming to understand how time allocation varies across different clients and projects. It calculates the average session length for each client over the last 14 days and prints these averages in a clear format.
Generated: 20260305_082213 UTC
"""

import pandas as pd
from supabase_helper import query_entries

df = pd.DataFrame(query_entries(days=14))
# Convert 'start' and 'stop' columns to datetime format for calculations
df['start'] = pd.to_datetime(df['start'])
df['stop'] = pd.to_datetime(df['stop'])
# Calculate session length in seconds
df['session_length'] = (df['stop'] - df['start']).dt.total_seconds()
# Group by client and calculate mean session length for each client
client_session_lengths = df.groupby('client_name')['session_length'].mean().reset_index()
print(client_session_lengths)
