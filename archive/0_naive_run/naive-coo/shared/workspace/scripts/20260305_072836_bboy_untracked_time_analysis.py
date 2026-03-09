"""Investigation: This script investigates the factors contributing to the high untracked time for BBOY by analyzing recent time-tracking data, converting 'start' and 'stop' columns to datetime format, calculating session lengths, and summing up the durations of BBOY sessions. It provides insights into potential issues such as distractions or unnoticed patterns that could impact time allocation.
Generated: 20260305_072836 UTC
"""

import pandas as pd
from supabase_helper import query_entries

days = 14
entries = query_entries(days=days)

dataframe = pd.DataFrame(entries)

dataframe['start'] = pd.to_datetime(dataframe['start'])

dataframe['stop'] = pd.to_datetime(dataframe['stop'])

dataframe['duration'] = (dataframe['stop'] - dataframe['start']).dt.total_seconds()

bboy_entries = dataframe[dataframe['client_name'] == 'BBOY']
bboy_untracked_time = bboy_entries['duration'].sum()

print(f'BBOY untracked time: {bboy_untracked_time} seconds')