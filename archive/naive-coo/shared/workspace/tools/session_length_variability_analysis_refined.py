"""Investigation: This script investigates the factors contributing to the session length variability across different clients over the last two weeks and assesses their impact on overall time allocation against target priorities. It calculates mean session lengths and standard deviations for each client, providing insights into potential imbalances or patterns that could inform adjustments to priorities or alert thresholds.
Generated: 20260306_000834 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

df = entries_to_dataframe(query_entries(days=14))
print(df.groupby('client_name')['duration_seconds'].mean())
print(df.groupby('client_name')['duration_seconds'].std())