"""Investigation: This script investigates the specific causes of the high untracked time for BBOY and proposes potential solutions to address these factors and improve time allocation.
Generated: 20260306_132928 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query recent entries for BBOY
entries = query_entries(days=7, client='BBOY')

# Convert entries to DataFrame
df = pd.DataFrame(entries)

# Calculate untracked time between sessions
untracked_time = []
for i in range(len(df) - 1):
    start_time = df.iloc[i]['stop']
    next_start_time = df.iloc[i+1]['start']
    untracked_time.append((next_start_time - start_time).total_seconds())

# Analyze untracked time patterns
average_untracked_time = sum(untracked_time) / len(untracked_time)
print(f'Average untracked time for BBOY: {average_untracked_time} seconds')

# Investigate potential causes of high untracked time
potential_causes = []
for entry in df['description']:
    if 'distraction' in entry or 'unnoticed pattern' in entry:
        potential_causes.append(entry)

print('Potential causes of high untracked time for BBOY:')
for cause in potential_causes:
    print(cause)
