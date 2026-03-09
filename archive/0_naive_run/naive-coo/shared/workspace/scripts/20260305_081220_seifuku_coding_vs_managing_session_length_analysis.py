"""Investigation: This script investigates the average session lengths for SEIFUKU tasks that involve coding versus managing, and compares these averages to the overall average session length for SEIFUKU. This analysis can provide insights into how different types of tasks within SEIFUKU contribute to its overall session length patterns.
Generated: 20260305_081220 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query recent time-tracking data
entries = query_entries(days=14)

# Create a DataFrame from the entries
df = pd.DataFrame(entries)

# Filter for SEIFUKU entries
seifuku_df = df[df['client_name'] == 'SEIFUKU']

# Define a function to convert duration strings to seconds
def duration_to_seconds(duration):
    hours, minutes, seconds = map(int, duration.split(':'))
    return hours * 3600 + minutes * 60 + seconds

# Apply the conversion to the 'duration' column
seifuku_df['duration_seconds'] = seifuku_df['duration'].apply(duration_to_seconds)

# Filter for coding and managing tasks within SEIFUKU
coding_tasks = seifuku_df[seifuku_df['tags'].str.contains('👾 Coding')]
managing_tasks = seifuku_df[seifuku_df['tags'].str.contains('⚙️ Managing')]

# Calculate the average session length for coding and managing tasks
avg_coding_session_length = coding_tasks['duration_seconds'].mean()
avg_managing_session_length = managing_tasks['duration_seconds'].mean()

# Calculate the overall average session length for SEIFUKU
overall_avg_seifuku_session_length = seifuku_df['duration_seconds'].mean()

# Print the findings
print(f'Average session length for SEIFUKU coding tasks: {avg_coding_session_length} seconds')
print(f'Average session length for SEIFUKU managing tasks: {avg_managing_session_length} seconds')
print(f'Overall average session length for SEIFUKU: {overall_avg_seifuku_session_length} seconds')
