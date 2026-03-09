"""Investigation: This script investigates the underlying causes of the differences in average session duration among clients by analyzing recent time-tracking data and calculating mean session durations for each client and project. It aims to understand how these differences impact overall time allocation against target priorities.
Generated: 20260305_161047 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

df = entries_to_dataframe(query_entries(days=14))
# Calculate average session duration for each client
client_avg_durations = df.groupby('client_name')['duration_seconds'].mean()
print(client_avg_durations)

categories = df['project_name'].unique()
for category in categories:
    cat_df = df[df['project_name'] == category]
    print(f'Category: {category}')
    print(cat_df.groupby('client_name')['duration_seconds'].mean())