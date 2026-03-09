"""Investigation: This script aims to refine the investigation strategy by identifying and addressing technical issues with data processing, such as missing values or incorrect data types, which have hindered deeper analyses of time allocation patterns.
Generated: 20260306_044743 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query recent entries
entries = query_entries(days=14)

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Identify potential technical issues
print('Checking for missing values:')
print(df.isnull().sum())

print('\
Checking data types:')
print(df.dtypes)

# Investigate 'duration' column specifically
duration_stats = df['duration_seconds'].describe()
print('\
Statistics of duration in seconds:')
print(duration_stats)

# Attempt to group by client and calculate mean session length
try:
    client_session_lengths = df.groupby('client_name')['duration_seconds'].mean()
    print('\
Mean session lengths by client (in seconds):')
    print(client_session_lengths)
except Exception as e:
    print(f'Error processing data: {e}')

# Save insights to a file for future reference
with open('/data/workspace/results/data_processing_insights.txt', 'w') as f:
    f.write('Data Processing Insights:\
')
    f.write(str(df.isnull().sum()) + '\
')
    f.write(str(df.dtypes) + '\
')
    f.write(str(duration_stats) + '\
')
    try:
        f.write(str(client_session_lengths) + '\
')
    except NameError:
        f.write('Failed to calculate mean session lengths by client.\
')

