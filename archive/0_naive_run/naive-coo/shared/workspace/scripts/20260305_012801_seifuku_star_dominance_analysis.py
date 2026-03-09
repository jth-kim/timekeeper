"""Investigation: This script investigates the underlying reasons for SEIFUKU's dominance and STAR's absence in the recent time-tracking data by calculating the total time spent on each client over the last 30 days.
Generated: 20260305_012801 UTC
"""

import pandas as pd
from supabase_helper import query_entries

df = pd.DataFrame(query_entries(days=30))
seifuku_df = df[df['client_name'] == 'SEIFUKU']
star_df = df[df['client_name'] == 'STAR']

# Calculate total time spent on SEIFUKU and STAR
seifuku_total_time = seifuku_df['duration'].sum()
star_total_time = star_df['duration'].sum()

# Print the results
print(f'Total time spent on SEIFUKU: {seifuku_total_time} seconds')
print(f'Total time spent on STAR: {star_total_time} seconds')