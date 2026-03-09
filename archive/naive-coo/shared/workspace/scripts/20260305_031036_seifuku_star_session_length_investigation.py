"""Investigation: This script investigates the cause of 'nan' values in the session length variability analysis for STAR and SEIFUKU by checking for non-numeric values in the 'duration' column, converting duration to seconds, and calculating mean session length and standard deviation for each client.
Generated: 20260305_031036 UTC
"""

import pandas as pd
from supabase_helper import query_entries

df = pd.DataFrame(query_entries(days=30))
print(df.head())
print(df.info())
print(df.describe())
# Check for non-numeric values in the 'duration' column
non_numeric_durations = df[~df['duration'].apply(lambda x: isinstance(x, (int, float)))]
print(non_numeric_durations)
# Convert duration to seconds and calculate mean session length and standard deviation for STAR and SEIFUKU
df['duration_seconds'] = pd.to_timedelta(df['duration']).dt.total_seconds()
star_sessions = df[df['client_name'] == 'STAR']
seifuku_sessions = df[df['client_name'] == 'SEIFUKU']
print(star_sessions['duration_seconds'].mean())
print(seifuku_sessions['duration_seconds'].mean())
print(star_sessions['duration_seconds'].std())
print(seifuku_sessions['duration_seconds'].std())