"""Investigation: This script investigates the underlying causes of significant untracked time gaps across clients, especially for SEIFUKU, by analyzing recent entries and calculating gaps between sessions.
Generated: 20260307_190121 UTC
"""


import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds

# Query recent entries to analyze untracked time
entries = query_entries(days=14)

# Convert entries to a DataFrame for easier analysis
df = pd.DataFrame(entries)

# Ensure 'start' and 'stop' columns are of datetime type
df['start'] = pd.to_datetime(df['start'])
df['stop'] = pd.to_datetime(df['stop'])

# Calculate session lengths in seconds
df['session_length_seconds'] = (df['stop'] - df['start']).dt.total_seconds()

# Sort entries by 'stop' time to calculate gaps between sessions
df_sorted = df.sort_values(by='stop')

# Initialize list to store gap durations
gaps = []

# Iterate over sorted entries to calculate gaps
for i in range(1, len(df_sorted)):
    gap = (df_sorted.iloc[i]['start'] - df_sorted.iloc[i-1]['stop']).total_seconds()
    gaps.append(gap)

# Calculate mean gap duration
mean_gap = sum(gaps) / len(gaps)

# Print findings
print(f'Mean gap duration between sessions: {mean_gap} seconds')
print('Gaps by client:')
for client in df['client_name'].unique():
    client_gaps = [gap for i, gap in enumerate(gaps) if df_sorted.iloc[i]['client_name'] == client]
    mean_client_gap = sum(client_gaps) / len(client_gaps)
    print(f'  {client}: {mean_client_gap} seconds')
