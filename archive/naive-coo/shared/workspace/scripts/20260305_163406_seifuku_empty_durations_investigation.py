"""Investigation: This script investigates the cause of the empty list of durations for SEIFUKU by querying recent entries, converting them to a DataFrame, and checking for empty or null duration values. If the list is indeed empty, it suggests a potential issue with data collection or processing that needs to be resolved.
Generated: 20260305_163406 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent entries for SEIFUKU
seifuku_entries = [entry for entry in query_entries(days=14) if entry['client_name'] == 'SEIFUKU']

# Convert to DataFrame
df = entries_to_dataframe(seifuku_entries)

# Check for empty duration list
if df.empty or df['duration_seconds'].isnull().all():
    print("The list of durations for SEIFUKU is empty. This could be due to no recent SEIFUKU entries or all entries having null durations.")
else:
    # Calculate average session duration for SEIFUKU
    avg_duration = df['duration_seconds'].mean()
    print(f"Average session duration for SEIFUKU: {avg_duration} seconds")
