"""Investigation: This script converts the 'duration' column from string format (HH:MM:SS) to a numeric format (seconds), enabling calculations such as mean duration for each client. It queries recent time-tracking data, creates a pandas dataframe, defines a function to convert duration strings to seconds, applies this conversion to the 'duration' column, and prints the first few rows of the resulting dataframe.
Generated: 20260305_062639 UTC
"""

import pandas as pd
from supabase_helper import query_entries

df = pd.DataFrame(query_entries(days=30))

def convert_duration_to_seconds(duration_str):
    h, m, s = map(int, duration_str.split(':'))
    return h * 3600 + m * 60 + s

df['duration'] = df['duration'].apply(convert_duration_to_seconds)
print(df.head())