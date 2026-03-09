"""Investigation: This script investigates the factors contributing to the variability in session length across different clients, particularly focusing on SEIFUKU's high self-transition rate. It queries the time-tracking data for the last 30 days, filters the entries for SEIFUKU, calculates the average session length, and then prints the result.
Generated: 20260305_013339 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query time-tracking data for the last 30 days
entries = query_entries(days=30)

# Convert entries to a pandas dataframe
df = pd.DataFrame(entries)

# Ensure 'duration' column is numeric
df['duration'] = pd.to_numeric(df['duration'])

# Filter dataframe for SEIFUKU entries
seifuku_df = df[df['client_name'] == 'SEIFUKU']

# Calculate average session length for SEIFUKU
avg_seifuku_session_length = seifuku_df['duration'].mean()

# Print the result
print(f'Average SEIFUKU session length: {avg_seifuku_session_length} seconds')

# Investigate factors contributing to variability in session length
# Calculate standard deviation of session lengths
std_dev_seifuku_session_length = seifuku_df['duration'].std()

# Print the result
print(f'Standard deviation of SEIFUKU session lengths: {std_dev_seifuku_session_length} seconds')

# Further analysis could involve plotting a histogram of session lengths or analyzing correlations with other variables
