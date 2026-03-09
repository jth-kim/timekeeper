"""Investigation: This script investigates the factors contributing to the prolonged absence of STAR activities and its impact on overall time allocation against target priorities. It queries recent entries for STAR, calculates the total time spent on other clients if there are no STAR entries, and compares it to the expected time for STAR based on the target allocation.
Generated: 20260305_141230 UTC
"""


import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds

# Query recent entries for STAR
entries = query_entries(days=14, client='STAR')

# If there are no recent STAR entries, calculate the total time spent on other clients
if not entries:
    all_entries = query_entries(days=14)
    df = pd.DataFrame(all_entries)
    df['duration_seconds'] = df['duration'].apply(parse_duration_seconds)
    total_time_other_clients = df['duration_seconds'].sum()
    
    # Calculate the expected time for STAR based on target allocation
    expected_star_time = 0.55 * total_time_other_clients / (1 - 0.55)
    
    print(f'Total time spent on other clients: {total_time_other_clients} seconds')
    print(f'Expected time for STAR: {expected_star_time} seconds')
else:
    # If there are recent STAR entries, calculate the average session length
    df = pd.DataFrame(entries)
    df['duration_seconds'] = df['duration'].apply(parse_duration_seconds)
    avg_session_length_star = df['duration_seconds'].mean()
    
    print(f'Average session length for STAR: {avg_session_length_star} seconds')
