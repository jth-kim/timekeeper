"""Investigation: This script investigates the factors contributing to the high session length variability within SEIFUKU and assesses their impact on overall time allocation against target priorities. It calculates the mean and standard deviation of session lengths for SEIFUKU, then groups entries by project name, tags, and description to identify potential factors influencing session length variability.
Generated: 20260306_033449 UTC
"""


import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds

# Query recent entries for SEIFUKU
entries = query_entries(days=30)
seifuku_entries = [entry for entry in entries if entry['client_name'] == 'SEIFUKU']

# Convert to DataFrame and calculate duration in seconds
df = pd.DataFrame(seifuku_entries)
df['duration_seconds'] = df['duration'].apply(parse_duration_seconds)

# Calculate session length variability
session_length_mean = df['duration_seconds'].mean()
session_length_std = df['duration_seconds'].std()

# Investigate factors contributing to high session length variability
factors = []
for column in ['project_name', 'tags', 'description']:
    groupby_df = df.groupby(column)['duration_seconds'].agg(['mean', 'std'])
    factors.append(groupby_df)

# Print findings
print('Session length mean:', session_length_mean)
print('Session length standard deviation:', session_length_std)
for factor in factors:
    print(factor)
