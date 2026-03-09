"""Investigation: This script investigates the factors contributing to the high average session duration in SEIFUKU and identifies opportunities for optimization to improve overall time allocation efficiency.
Generated: 20260306_100559 UTC
"""


import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds

# Query recent entries for SEIFUKU
entries = query_entries(days=14)
seifuku_entries = [entry for entry in entries if entry['client_name'] == 'SEIFUKU']

# Convert to DataFrame and calculate session durations
df = pd.DataFrame(seifuku_entries)
df['duration_seconds'] = df['duration'].apply(parse_duration_seconds)

# Calculate average session duration for SEIFUKU
avg_session_duration = df['duration_seconds'].mean()

# Identify top 5 tasks by duration within SEIFUKU
top_tasks = df.groupby('project_name')['duration_seconds'].sum().sort_values(ascending=False).head(5)

# Print findings
print(f'Average session duration for SEIFUKU: {avg_session_duration} seconds')
print('Top 5 tasks by duration within SEIFUKU:')
print(top_tasks)
