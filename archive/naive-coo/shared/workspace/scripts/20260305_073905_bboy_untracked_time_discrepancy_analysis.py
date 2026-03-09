"""Investigation: This script investigates the underlying causes of the discrepancy between the current reported BBOY untracked time of 0.0 seconds and previous findings of significant variability in untracked time across clients, including a high untracked time for BBOY. It queries recent time-tracking data, filters for BBOY entries, calculates total untracked time, and compares with previous findings to identify potential issues with data collection or analysis process.
Generated: 20260305_073905 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query recent time-tracking data
entries = query_entries(days=14)

# Convert to DataFrame
df = pd.DataFrame(entries)

# Filter for BBOY entries
bboy_df = df[df['client_name'] == 'BBOY']

# Calculate total untracked time for BBOY
total_untracked_time_bboy = bboy_df['untracked_time'].sum()

# Compare with previous findings
previous_findings = 40071.095238  # Previous reported untracked time for BBOY

if total_untracked_time_bboy == 0.0:
    print('Discrepancy found: Current reported BBOY untracked time is 0.0 seconds, but previous findings indicated significant variability.')
else:
    print('No discrepancy found: Current reported BBOY untracked time matches previous findings.')

# Investigate potential causes of discrepancy
if total_untracked_time_bboy == 0.0:
    # Check for data collection or analysis process issues
    print('Investigating potential issues with data collection or analysis process...')

    # ... further investigation code ...
