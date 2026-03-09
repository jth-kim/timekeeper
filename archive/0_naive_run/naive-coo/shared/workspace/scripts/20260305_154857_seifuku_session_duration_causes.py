"""Investigation: This script investigates the underlying causes of SEIFUKU's high average session duration by analyzing the durations of individual projects within SEIFUKU. It calculates the average session duration for SEIFUKU and prints the average durations for each project, providing insights into potential factors contributing to the high average session duration.
Generated: 20260305_154857 UTC
"""

import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds

df = pd.DataFrame(query_entries(days=14))
seifuku_entries = df[df['client_name'] == 'SEIFUKU']
seifuku_durations = seifuku_entries['duration'].apply(parse_duration_seconds)
average_seifuku_duration = seifuku_durations.mean()
print(f'Average SEIFUKU session duration: {average_seifuku_duration} seconds')

# Investigate causes of high average session duration
seifuku_project_durations = seifuku_entries.groupby('project_name')['duration'].apply(lambda x: parse_duration_seconds(x.iloc[0]))
print(seifuku_project_durations)
