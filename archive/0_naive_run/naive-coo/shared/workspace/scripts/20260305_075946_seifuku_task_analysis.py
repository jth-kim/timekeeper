"""Investigation: This script investigates the specific tasks or activities within SEIFUKU that contribute to its longer session lengths, aiming to optimize or manage these tasks for improved overall productivity.
Generated: 20260305_075946 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query recent time-tracking data
entries = query_entries(days=14)

# Convert to DataFrame
df = pd.DataFrame(entries)

# Filter for SEIFUKU entries
seifuku_df = df[df['client_name'] == 'SEIFUKU']

# Calculate session lengths in seconds
seifuku_df['session_length'] = seifuku_df['duration'].apply(lambda x: int(x.split(':')[0]) * 3600 + int(x.split(':')[1]) * 60 + int(x.split(':')[2]))

# Group by project_name and calculate average session length
project_avg_session_lengths = seifuku_df.groupby('project_name')['session_length'].mean()

# Print results
print(project_avg_session_lengths)
