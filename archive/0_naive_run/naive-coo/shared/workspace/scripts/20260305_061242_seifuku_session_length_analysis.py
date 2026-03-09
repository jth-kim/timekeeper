"""Investigation: This script analyzes the factors contributing to the significant variability in session lengths for SEIFUKU across different tasks, such as coding versus managing. It ensures that the 'duration' column exists and is in a suitable format for analysis, then calculates the average session lengths for each task within SEIFUKU.
Generated: 20260305_061242 UTC
"""

import pandas as pd
from supabase_helper import query_entries

df = pd.DataFrame(query_entries(days=30))
# Ensure 'duration' column exists and is in suitable format for analysis
if 'duration' not in df.columns:
    print("'duration' column does not exist in the dataframe.")
else:
    # Convert duration to seconds if it's not already
    def convert_duration_to_seconds(duration):
        hours, minutes, seconds = map(int, duration.split(':'))
        return hours * 3600 + minutes * 60 + seconds
    
df['duration_seconds'] = df['duration'].apply(convert_duration_to_seconds)
    # Group by client and task to calculate average session lengths
    seifuku_df = df[df['client_name'] == 'SEIFUKU']
    average_session_lengths = seifuku_df.groupby('tags')['duration_seconds'].mean()
    print(average_session_lengths)