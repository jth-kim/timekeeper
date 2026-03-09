"""Investigation: This script analyzes the recent entries under SEIFUKU to identify patterns and tasks that contribute to its long average session length, providing insights into how these might impact overall time allocation.
Generated: 20260305_043149 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query recent entries for SEIFUKU
entries = query_entries(days=14)
seifuku_entries = [entry for entry in entries if entry['client_name'] == 'SEIFUKU']

# Convert to DataFrame
df = pd.DataFrame(seifuku_entries)

# Calculate average session length by project
avg_session_length_by_project = df.groupby('project_name')['duration'].mean()

# Print findings
print('Average session length by project for SEIFUKU:')
print(avg_session_length_by_project)

# Investigate tasks within SEIFUKU contributing to long sessions
long_sessions = df[df['duration'] > avg_session_length_by_project.max()]
print('\
Tasks in longest sessions for SEIFUKU:')
print(long_sessions['description'])
