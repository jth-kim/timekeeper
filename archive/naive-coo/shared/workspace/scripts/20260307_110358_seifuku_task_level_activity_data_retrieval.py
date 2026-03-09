"""Investigation: This script investigates the technical reasons behind the empty DataFrames in recent scripts and modifies the data retrieval process to successfully retrieve task-level activity data for SEIFUKU. It queries the time-tracking data for the last 14 days, converts it into a pandas DataFrame, filters for SEIFUKU entries, and calculates the mean session length for each day of the week.
Generated: 20260307_110358 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query entries for the last 14 days
entries = query_entries(days=14)

# Convert entries to a DataFrame with proper types
df = entries_to_dataframe(entries)

# Filter for SEIFUKU entries
seifuku_df = df[df['client_name'] == 'SEIFUKU']

# Check if seifuku_df is empty
if seifuku_df.empty:
    print('No SEIFUKU entries found in the last 14 days.')
else:
    # Calculate mean session length for each day of the week
    seifuku_df['start'] = pd.to_datetime(seifuku_df['start'])
    seifuku_df['day_of_week'] = seifuku_df['start'].dt.day_name()
    mean_session_lengths = seifuku_df.groupby('day_of_week')['duration_seconds'].mean()

    # Print the results
    print(mean_session_lengths)
