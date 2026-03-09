"""Investigation: This script investigates the underlying causes of the high standard deviations in session lengths for STAR and SEIFUKU by correcting the data quality or processing issues causing the 'nan' values in the script output. It queries the time-tracking data, converts the duration column to numeric values, drops any rows with missing duration values, filters the data for STAR and SEIFUKU entries, and calculates the mean session length for each client.
Generated: 20260305_031815 UTC
"""

import pandas as pd
from supabase_helper import query_entries

df = pd.DataFrame(query_entries(days=30))

df['duration'] = pd.to_numeric(df['duration'], errors='coerce')

df.dropna(subset=['duration'], inplace=True)

star_df = df[df['client_name'] == 'STAR']
seifuku_df = df[df['client_name'] == 'SEIFUKU']

print(star_df['duration'].mean())
print(seifuku_df['duration'].mean())