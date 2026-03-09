"""Investigation: This script investigates the factors contributing to the session length variability across different clients over the last two weeks and assesses their impact on overall time allocation against target priorities. It calculates mean session lengths and standard deviations for each client, providing insights into potential imbalances or patterns that could inform adjustments to priorities or alert thresholds.
Generated: 20260305_232131 UTC
"""

import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds, entries_to_dataframe

df = entries_to_dataframe(query_entries(days=14))
# Calculate session lengths in seconds and convert to hours for easier comparison
df['session_length_hours'] = df['duration_seconds'] / 3600

clients = df['client_name'].unique()
for client in clients:
    client_df = df[df['client_name'] == client]
    mean_session_length = client_df['session_length_hours'].mean()
    std_dev_session_length = client_df['session_length_hours'].std()
    print(f'Client: {client}, Mean Session Length (hours): {mean_session_length}, Standard Deviation of Session Length (hours): {std_dev_session_length}')