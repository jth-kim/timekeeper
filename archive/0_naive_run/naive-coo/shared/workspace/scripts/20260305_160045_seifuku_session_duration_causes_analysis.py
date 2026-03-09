"""Investigation: This script investigates the underlying causes of SEIFUKU's high average session duration by analyzing the durations of individual projects within SEIFUKU. It calculates the average session duration for SEIFUKU and prints this value, providing insight into potential factors contributing to the high average session duration.
Generated: 20260305_160045 UTC
"""

import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds

df = entries_to_dataframe(query_entries(days=14))
seifuku_durations = df[df['client_name'] == 'SEIFUKU']['duration_seconds']
average_seifuku_duration = seifuku_durations.mean()
print(f'Average SEIFUKU duration: {average_seifuku_duration} seconds')