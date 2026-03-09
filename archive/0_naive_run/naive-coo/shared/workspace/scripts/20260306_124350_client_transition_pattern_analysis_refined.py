"""Investigation: This script investigates client transition patterns across sessions over the last week, including how often each client follows another and what this means for overall time allocation. It queries recent entries, converts them to a DataFrame, calculates session lengths and transitions, and prints these findings.
Generated: 20260306_124350 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query recent entries (last week)
entries = query_entries(days=7)

# Convert to DataFrame with proper types
df = pd.DataFrame(entries)

# Define function to convert duration strings to seconds
def parse_duration_seconds(duration_str):
    from datetime import timedelta
    delta = timedelta(seconds=0)
    if 'H' in duration_str:
        hours = int(duration_str.split('PT')[1].split('H')[0])
        delta += timedelta(hours=hours)
        duration_str = duration_str.split('H')[1]
    if 'M' in duration_str:
        minutes = int(duration_str.split('M')[0])
        delta += timedelta(minutes=minutes)
        duration_str = duration_str.split('M')[1]
    if 'S' in duration_str:
        seconds = int(duration_str.split('S')[0])
        delta += timedelta(seconds=seconds)
    return delta.total_seconds()

# Apply conversion to 'duration' column
df['duration_seconds'] = df['duration'].apply(parse_duration_seconds)

# Calculate session lengths and transitions
session_lengths = df.groupby('client_name')['duration_seconds'].sum()
transitions = df[['client_name', 'project_name']].shift().fillna('None')

# Print findings
print('Session Lengths:')
print(session_lengths)
print('\
Transitions:')
print(transitions)