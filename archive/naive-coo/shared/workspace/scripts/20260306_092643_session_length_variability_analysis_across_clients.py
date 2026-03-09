"""Investigation: This script investigates the factors contributing to the variability in session lengths across different clients over the last two weeks and assesses their impact on overall time allocation against target priorities. It calculates mean session lengths for each client, providing insights into potential imbalances or patterns that could inform adjustments to priorities or alert thresholds.
Generated: 20260306_092643 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

df = entries_to_dataframe(query_entries(days=14))
# Calculate session lengths in seconds and group by client
session_lengths = df.groupby('client_name')['duration_seconds'].mean().reset_index()
print(session_lengths)
# Perform statistical analysis to identify factors contributing to variability
import statistics
for client, group in df.groupby('client_name'):
    print(f'Client: {client}')
    print(f'Mean session length: {statistics.mean(group[