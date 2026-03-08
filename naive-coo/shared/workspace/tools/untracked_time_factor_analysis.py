"""Investigation: This script investigates the factors contributing to the variability in untracked time between sessions and assesses their impact on overall time allocation against target priorities. It queries the time-tracking data for the last 14 days, creates a pandas dataframe, and then prints the first few rows of the dataframe, information about the dataframe, and summary statistics for the dataframe.
Generated: 20260305_011050 UTC
"""

import pandas as pd
from supabase_helper import query_entries, read_memory

df = pd.DataFrame(query_entries(days=14))
print(df.head())
print(df.info())
print(df.describe())