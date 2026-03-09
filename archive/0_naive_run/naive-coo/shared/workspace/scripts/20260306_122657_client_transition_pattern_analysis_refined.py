"""Investigation: This script investigates client transition patterns across sessions over the last week. It calculates how often each client follows another and discusses what this means for overall time allocation. The goal is to understand sequencing in the Sovereign's work schedule and its impact on meeting long-term goals.
Generated: 20260306_122657 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query recent entries (last week)
entries = query_entries(days=7)

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Ensure 'start' and 'stop' are datetime for time calculations
df['start'] = pd.to_datetime(df['start'])
df['stop'] = pd.to_datetime(df['stop'])

# Calculate session duration in seconds (to handle easier)
df['duration_seconds'] = df.apply(lambda row: (row['stop'] - row['start']).total_seconds(), axis=1)

# Initialize a dictionary to hold transition counts
transition_counts = {}

# Iterate through rows to find transitions
for index, row in df.iterrows():
    # If this is not the first entry and the 'client_name' differs from the previous one
    if index > 0:
        prev_row = df.iloc[index - 1]
        if row['client_name'] != prev_row['client_name']:
            # Create a transition key (prev_client -> current_client)
            transition_key = f