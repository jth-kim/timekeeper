"""Investigation: This script investigates the factors contributing to the variability in session lengths across different clients and assesses their impact on overall time allocation against target priorities. By analyzing recent time-tracking data, it calculates average session lengths and standard deviations for each client, providing insights into potential imbalances or patterns that could inform adjustments to the alert thresholds configuration.
Generated: 20260305_030057 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query recent entries (e.g., last 30 days)
entries = query_entries(days=30)

# Convert to DataFrame for easier analysis
df = pd.DataFrame(entries)

# Ensure 'start' and 'stop' columns are datetime type
df['start'] = pd.to_datetime(df['start'])
df['stop'] = pd.to_datetime(df['stop'])

# Calculate session length in seconds (more precise than minutes or hours)
df['session_length_seconds'] = (df['stop'] - df['start']).dt.total_seconds()

# Group by client and calculate mean, std of session lengths
client_session_lengths = df.groupby('client_name')['session_length_seconds'].agg(['mean', 'std'])

# Print findings to stdout in a clear format
print('Session Length Variability Across Clients:')
print(client_session_lengths)

# Further investigation: Identify clients with high variability (std > mean)
high_variability_clients = client_session_lengths[client_session_lengths['std'] > client_session_lengths['mean']]
if not high_variability_clients.empty:
    print('\
Clients with High Session Length Variability:')
    print(high_variability_clients)
else:
    print('\
No clients show significantly high session length variability.')
