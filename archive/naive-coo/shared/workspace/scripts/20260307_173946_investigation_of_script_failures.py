"""Investigation: This script investigates the root cause of recent script failures by analyzing the data processing pipeline and identifying potential issues with data types or missing values. It queries the time-tracking data for the last 14 days, converts it to a pandas DataFrame, and then prints information about the dataframe to identify any potential problems.
Generated: 20260307_173946 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

df = entries_to_dataframe(query_entries(days=14))
print(df.head())
print(df.info())
print(df.describe())