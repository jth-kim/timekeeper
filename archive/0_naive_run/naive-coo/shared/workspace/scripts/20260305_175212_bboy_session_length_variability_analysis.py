"""Investigation: This script investigates the underlying causes of the variability in session lengths across different projects for BBOY and assesses its impact on the Sovereign's ability to meet target allocations for other clients. It calculates average session lengths and standard deviations for each project within BBOY, providing insights into potential imbalances or patterns that could inform adjustments to priorities or alert thresholds.
Generated: 20260305_175212 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data for BBOY
entries = query_entries(days=14)
bboy_entries = [entry for entry in entries if entry['client_name'] == 'BBOY']

# Convert to DataFrame with proper types
df = entries_to_dataframe(bboy_entries)

# Calculate average session length for each project within BBOY
project_avg_session_lengths = df.groupby('project_name')['duration_seconds'].mean()

# Print the results
print('Average session lengths for BBOY projects:')
print(project_avg_session_lengths)

# Investigate the variability in session lengths across different projects for BBOY
project_std_devs = df.groupby('project_name')['duration_seconds'].std()
print('\
Standard deviations of session lengths for BBOY projects:')
print(project_std_devs)
