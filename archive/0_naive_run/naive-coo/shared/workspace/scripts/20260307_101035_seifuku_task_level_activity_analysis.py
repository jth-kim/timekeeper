"""Investigation: This script investigates task-level activity patterns within SEIFUKU, aiming to understand what contributes to its high session duration and how these activities align with the Sovereign's broader objectives.
Generated: 20260307_101035 UTC
"""


import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds

# Query recent entries for SEIFUKU
entries = query_entries(days=14)
seifuku_entries = [entry for entry in entries if entry['client_name'] == 'SEIFUKU']

# Convert durations to seconds and extract task descriptions
data = []
for entry in seifuku_entries:
    duration_seconds = parse_duration_seconds(entry['duration'])
    data.append({
        'description': entry['description'],
        'duration_seconds': duration_seconds
    })

# Create a DataFrame for analysis
df = pd.DataFrame(data)

# Group by description and calculate mean duration
mean_durations = df.groupby('description')['duration_seconds'].mean()

# Print the results
print(mean_durations)
