"""Investigation: This script investigates the task-level activities within STAR that contribute to its prolonged session durations and assesses their alignment with the Sovereign's objectives. It queries recent entries for STAR, converts them to a DataFrame, and prints the first few rows of the DataFrame, information about the DataFrame, and summary statistics for the DataFrame.
Generated: 20260306_140632 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

df = entries_to_dataframe(query_entries(days=14, client='STAR'))
print(df.head())
print(df.info())
print(df.describe())