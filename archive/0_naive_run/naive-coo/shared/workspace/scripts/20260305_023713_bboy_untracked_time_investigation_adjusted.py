"""Investigation: This script investigates the cause of the ZeroDivisionError when calculating average untracked time for BBOY and ensures that the data used for this calculation is complete and accurate. It filters out non-numeric duration values, calculates untracked time between BBOY sessions, and prints the average untracked time if it exists.
Generated: 20260305_023713 UTC
"""

import pandas as pd
from supabase_helper import query_entries

days = 14
entries = query_entries(days=days)

# Ensure 'duration' is numeric and filter out non-numeric values
for entry in entries:
    try:
        entry['duration'] = float(entry['duration'])
    except ValueError:
        print(f"Non-numeric duration found: {entry['duration']}")
        entries.remove(entry)

# Filter for BBOY entries
bboy_entries = [entry for entry in entries if entry['client_name'] == 'BBOY']

if not bboy_entries:
    print("No BBOY entries found.")
else:
    # Calculate untracked time between sessions
    untracked_time = []
    for i in range(len(bboy_entries) - 1):
        start_time = pd.to_datetime(bboy_entries[i]['stop'])
        next_start_time = pd.to_datetime(bboy_entries[i+1]['start'])
        untracked_time.append((next_start_time - start_time).total_seconds())
    
    if not untracked_time:
        print("No untracked time found between BBOY sessions.")
    else:
        average_untracked_time = sum(untracked_time) / len(untracked_time)
        print(f"Average untracked time for BBOY: {average_untracked_time} seconds")