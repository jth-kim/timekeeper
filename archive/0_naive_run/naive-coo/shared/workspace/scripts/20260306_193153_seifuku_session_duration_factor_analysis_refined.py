"""Investigation: This script investigates the factors contributing to the high average session duration in SEIFUKU by analyzing recent time-tracking data, calculating statistics such as mean and standard deviation of session durations, and examining task-level activities within SEIFUKU. The goal is to understand how these factors impact overall productivity and goal achievement.
Generated: 20260306_193153 UTC
"""

import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds, entries_to_dataframe

df = entries_to_dataframe(query_entries(days=14))
seifuku_df = df[df['client_name'] == 'SEIFUKU']
print(seifuku_df.head())
print(seifuku_df.describe())