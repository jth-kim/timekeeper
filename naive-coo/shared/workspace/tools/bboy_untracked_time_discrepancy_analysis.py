"""Investigation: This script investigates the underlying causes of the discrepancy between the reported BBOY untracked time and previous findings, and assesses its impact on the Sovereign's ability to meet target allocations for other clients.
Generated: 20260305_185352 UTC
"""


import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds

# Get recent entries
entries = query_entries(days=30)

# Convert entries to DataFrame
df = pd.DataFrame(entries)

# Calculate total time spent on BBOY
bboy_time = df[df['client_name'] == 'BBOY']['duration'].apply(parse_duration_seconds).sum()

# Calculate expected total time based on target allocation
expected_bboy_time = 0.2 * (df['duration'].apply(parse_duration_seconds).sum())

# Calculate discrepancy
discrepancy = bboy_time - expected_bboy_time

print(f'Discrepancy: {discrepancy} seconds')
