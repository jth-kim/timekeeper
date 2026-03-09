"""Investigation: This script investigates the underlying causes of the prolonged absence of STAR activities and its impact on overall time allocation against target priorities. It calculates the total time spent on STAR, average session length, and deviation from target allocation.
Generated: 20260305_150759 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query recent entries for STAR
entries = query_entries(days=30)
star_entries = [entry for entry in entries if entry['client_name'] == 'STAR']

# Calculate total time spent on STAR
total_star_time = sum(parse_duration_seconds(entry['duration']) for entry in star_entries)

# Calculate average session length for STAR
average_star_session_length = total_star_time / len(star_entries) if star_entries else 0

# Print findings
print(f'Total time spent on STAR: {total_star_time} seconds')
print(f'Average session length for STAR: {average_star_session_length} seconds')

# Calculate deviation from target allocation
target_allocation = 0.55
actual_allocation = total_star_time / sum(parse_duration_seconds(entry['duration']) for entry in entries)
deviation = actual_allocation - target_allocation

# Print deviation
print(f'Deviation from target allocation: {deviation}')
