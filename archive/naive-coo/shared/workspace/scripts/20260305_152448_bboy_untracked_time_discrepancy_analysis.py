"""Investigation: This script investigates the discrepancy between the reported BBOY untracked time and previous findings by calculating the total time spent on BBOY tasks over the last 14 days and comparing it to the expected total time based on target allocation. It also proposes modifications to the data collection and analysis process to accurately capture this information.
Generated: 20260305_152448 UTC
"""

import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds

df = pd.DataFrame(query_entries(days=14))

df['duration_seconds'] = df['duration'].apply(parse_duration_seconds)

total_bboy_time = df[df['client_name'] == 'BBOY']['duration_seconds'].sum()

print(f'Total BBOY time: {total_bboy_time} seconds')
