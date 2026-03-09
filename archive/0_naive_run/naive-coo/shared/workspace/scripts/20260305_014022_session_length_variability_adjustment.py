"""Investigation: This script investigates the factors contributing to the variability in session length across different clients by adjusting the dataframe to ensure the 'duration' column is of the correct data type for analysis and calculating average session lengths and standard deviations for each client.
Generated: 20260305_014022 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query recent entries
entries = query_entries(days=30)

# Convert duration to numeric values
def convert_duration(duration):
    if ':' in duration:
        hours, minutes, seconds = map(int, duration.split(':'))
        return hours * 3600 + minutes * 60 + seconds
    else:
        return float(duration)

# Create dataframe with converted durations
df = pd.DataFrame(entries)
df['duration'] = df['duration'].apply(convert_duration)

# Calculate session length variability for each client
client_variability = {}
for client in df['client_name'].unique():
    client_df = df[df['client_name'] == client]
    avg_session_length = client_df['duration'].mean()
    std_dev = client_df['duration'].std()
    client_variability[client] = (avg_session_length, std_dev)

# Print results
for client, stats in client_variability.items():
    print(f'Client: {client}, Average Session Length: {stats[0]} seconds, Standard Deviation: {stats[1]} seconds')
