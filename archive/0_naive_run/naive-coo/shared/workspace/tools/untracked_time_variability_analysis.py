"""Investigation: This script analyzes the variability in untracked time between sessions over the last week and its impact on overall time allocation against target priorities.
Generated: 20260304_230017 UTC
"""

import pandas as pd
from supabase_helper import query_entries

df = pd.DataFrame(query_entries(days=7))

df['start'] = pd.to_datetime(df['start'])
df['stop'] = pd.to_datetime(df['stop'])

df['duration'] = df['stop'] - df['start']

gaps = []
for i in range(len(df) - 1):
    gap = (df.iloc[i+1]['start'] - df.iloc[i]['stop']).total_seconds() / 3600
    gaps.append(gap)

gaps_df = pd.DataFrame(gaps, columns=['gap'])
print(gaps_df.describe())