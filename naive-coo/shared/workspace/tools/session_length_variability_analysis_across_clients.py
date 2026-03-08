"""Investigation: This script investigates the factors contributing to the variability in session lengths across different clients over the last two weeks. It calculates mean session lengths and standard deviations for each client, providing insights into potential imbalances or patterns that could inform adjustments to priorities or alert thresholds.
Generated: 20260305_172445 UTC
"""


from supabase_helper import query_entries, entries_to_dataframe
import pandas as pd

# Query recent time-tracking data for the last 14 days
entries = query_entries(days=14)

# Convert entries to a DataFrame with proper types
df = entries_to_dataframe(entries)

# Group by client name and calculate mean session lengths
mean_session_lengths = df.groupby('client_name')['duration_seconds'].mean()

# Calculate standard deviations of session lengths for each client
std_devs = df.groupby('client_name')['duration_seconds'].std()

# Print findings
print('Mean Session Lengths:')
print(mean_session_lengths)
print('\
Standard Deviations:')
print(std_devs)

# Save results to a file for future reference
with open('/data/workspace/results/session_length_variability.txt', 'w') as f:
    f.write(str(mean_session_lengths) + '\
\
' + str(std_devs))
