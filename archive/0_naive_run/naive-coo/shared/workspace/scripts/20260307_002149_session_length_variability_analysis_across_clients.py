"""Investigation: This script investigates the factors contributing to session length variability across different clients over the last 14 days. It calculates the average session duration for each client, providing insights into potential imbalances or patterns that could inform adjustments to priorities or alert thresholds.
Generated: 20260307_002149 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

df = entries_to_dataframe(query_entries(days=14))
# Calculate session length for each entry and convert to seconds
session_lengths = df['duration_seconds']
# Group by client and calculate mean session length
mean_session_lengths = session_lengths.groupby(df['client_name']).mean()
print(mean_session_lengths)