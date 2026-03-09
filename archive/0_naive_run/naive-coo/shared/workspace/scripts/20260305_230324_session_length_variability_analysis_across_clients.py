"""Investigation: This script investigates the factors contributing to the variability in session lengths across different clients over the last two weeks and assesses their impact on overall time allocation against target priorities. It calculates mean session lengths and standard deviations for each client, providing insights into potential imbalances or patterns that could inform adjustments to priorities or alert thresholds.
Generated: 20260305_230324 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

days = 14
entries = query_entries(days=days)
dataframe = entries_to_dataframe(entries)

clients = dataframe['client_name'].unique()
for client in clients:
    client_data = dataframe[dataframe['client_name'] == client]
    mean_session_length = client_data['duration_seconds'].mean()
    std_dev_session_length = client_data['duration_seconds'].std()
    print(f'Client: {client}, Mean Session Length: {mean_session_length}, Standard Deviation: {std_dev_session_length}')