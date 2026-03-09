"""Investigation: This script investigates the root causes of the missing 'duration' column in the data frame and proposes modifications to the data collection or processing pipeline to prevent such errors in the future.
Generated: 20260306_013918 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query recent entries
entries = query_entries(days=14)

# Convert entries to DataFrame
df = entries_to_dataframe(entries)

# Check for missing 'duration' column
if 'duration_seconds' not in df.columns:
    print("'duration_seconds' column is missing")
else:
    print("'duration_seconds' column exists")

# Investigate the root cause of the missing 'duration' column
if df['duration'].isnull().any():
    print("There are null values in the 'duration' column")
else:
    print("There are no null values in the 'duration' column")

# Modify the data collection or processing pipeline to prevent such errors
def parse_duration(duration_str):
    if duration_str is None or pd.isnull(duration_str):
        return 0
    else:
        return parse_duration_seconds(duration_str)

df['duration_seconds'] = df['duration'].apply(parse_duration)
