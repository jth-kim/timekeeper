"""Investigation: This script investigates the factors contributing to the session length variability across different clients over the last two weeks and assesses their impact on overall time allocation against target priorities. It calculates mean session lengths and standard deviations for each client, providing insights into potential imbalances or patterns that could inform adjustments to priorities or alert thresholds.
Generated: 20260305_233306 UTC
"""

import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds, entries_to_dataframe

days = 14
entries = query_entries(days=days)
dataframe = entries_to_dataframe(entries)

dataframe['client_name'] = dataframe['client_name'].astype('category')
mean_session_lengths = dataframe.groupby('client_name')['duration_seconds'].mean()
std_dev_session_lengths = dataframe.groupby('client_name')['duration_seconds'].std()
print(mean_session_lengths)
print(std_dev_session_lengths)