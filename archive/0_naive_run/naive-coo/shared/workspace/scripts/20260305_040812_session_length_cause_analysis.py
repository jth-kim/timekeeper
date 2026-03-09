"""Investigation: This script investigates the underlying causes of significant differences in average session lengths between clients and projects, analyzing statistics such as standard deviation, minimum, and maximum session lengths to understand these differences and their impact on overall time allocation.
Generated: 20260305_040812 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query recent entries
entries = query_entries(days=14)

# Convert to dataframe
df = pd.DataFrame(entries)

# Ensure 'start' and 'stop' are datetime
df['start'] = pd.to_datetime(df['start'])
df['stop'] = pd.to_datetime(df['stop'])

# Calculate session length in seconds
df['session_length'] = (df['stop'] - df['start']).dt.total_seconds()

# Group by client and project, calculate mean session length
mean_session_lengths = df.groupby(['client_name', 'project_name'])['session_length'].mean().reset_index()

# Print results
print(mean_session_lengths)

# Investigate causes of differences in average session lengths
for index, row in mean_session_lengths.iterrows():
    client = row['client_name']
    project = row['project_name']
    avg_session_length = row['session_length']
    
    # Filter entries for this client and project
    client_project_entries = df[(df['client_name'] == client) & (df['project_name'] == project)]
    
    # Calculate statistics on session lengths
    std_dev = client_project_entries['session_length'].std()
    min_session = client_project_entries['session_length'].min()
    max_session = client_project_entries['session_length'].max()
    
    print(f'Client: {client}, Project: {project}')
    print(f'Average Session Length: {avg_session_length} seconds')
    print(f'Standard Deviation: {std_dev} seconds')
    print(f'Minimum Session Length: {min_session} seconds')
    print(f'Maximum Session Length: {max_session} seconds')
    print('---')
  