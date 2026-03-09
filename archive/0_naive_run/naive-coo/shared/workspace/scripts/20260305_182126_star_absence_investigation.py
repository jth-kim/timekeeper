"""Investigation: This script investigates the prolonged absence of STAR activities and its impact on overall time allocation. It calculates the total time spent on STAR, compares it to the target allocation, and prints the results.
Generated: 20260305_182126 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query recent entries for STAR
entries = query_entries(days=14)
star_entries = [entry for entry in entries if entry['client_name'] == 'STAR']

# Calculate total time spent on STAR
total_star_time = sum(parse_duration_seconds(entry['duration']) for entry in star_entries)

# Compare to target allocation
target_allocation = 0.55
actual_allocation = total_star_time / sum(parse_duration_seconds(entry['duration']) for entry in entries)

print(f'Total time spent on STAR: {total_star_time} seconds')
print(f'Actual allocation: {actual_allocation:.2f}')
print(f'Target allocation: {target_allocation:.2f}')

if actual_allocation < target_allocation:
    print('STAR activities are below target allocation.')
else:
    print('STAR activities are at or above target allocation.')
