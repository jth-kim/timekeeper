"""Investigation: This script investigates the factors contributing to the variability in session lengths across different projects for BBOY, aiming to understand how this variability impacts the Sovereign's ability to meet target allocations for other clients. It queries recent time-tracking data, filters for BBOY entries, and calculates the mean session length for each project.
Generated: 20260305_185908 UTC
"""


import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds

# Query recent entries
entries = query_entries(days=30)

# Convert durations to seconds and create a dataframe
df = pd.DataFrame(entries)
df['duration_seconds'] = df['duration'].apply(parse_duration_seconds)

# Filter for BBOY entries
bboy_df = df[df['client_name'] == 'BBOY']

# Group by project and calculate mean session length
project_session_lengths = bboy_df.groupby('project_name')['duration_seconds'].mean()

# Print the results
print(project_session_lengths)
