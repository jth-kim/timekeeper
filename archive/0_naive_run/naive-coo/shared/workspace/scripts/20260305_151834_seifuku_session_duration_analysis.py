"""Investigation: This script investigates the factors contributing to the high average session duration for SEIFUKU compared to other clients and assesses its impact on overall time allocation against target priorities. It calculates the average session duration for SEIFUKU, compares it to other clients, and investigates the specific activities within SEIFUKU that contribute to this high average session duration.
Generated: 20260305_151834 UTC
"""


import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds

# Query recent entries for SEIFUKU
entries = query_entries(days=14, client='SEIFUKU')

# Convert entries to DataFrame
df = pd.DataFrame(entries)

# Calculate average session duration for SEIFUKU
average_session_duration_seifuku = df['duration'].apply(parse_duration_seconds).mean()

# Query recent entries for other clients
other_client_entries = query_entries(days=14, client=['STAR', 'BBOY', 'BOJ'])

# Convert entries to DataFrame
other_client_df = pd.DataFrame(other_client_entries)

# Calculate average session duration for other clients
average_session_duration_other_clients = other_client_df['duration'].apply(parse_duration_seconds).mean()

# Compare average session durations
if average_session_duration_seifuku > average_session_duration_other_clients:
    print('SEIFUKU has a higher average session duration compared to other clients.')
else:
    print('SEIFUKU does not have a higher average session duration compared to other clients.')

# Investigate factors contributing to high average session duration for SEIFUKU
seifuku_coding_entries = query_entries(days=14, client='SEIFUKU', project='Artemis')
seifuku_coding_df = pd.DataFrame(seifuku_coding_entries)
average_session_duration_seifuku_coding = seifuku_coding_df['duration'].apply(parse_duration_seconds).mean()

seifuku_managing_entries = query_entries(days=14, client='SEIFUKU', project='Self authoring')
seifuku_managing_df = pd.DataFrame(seifuku_managing_entries)
average_session_duration_seifuku_managing = seifuku_managing_df['duration'].apply(parse_duration_seconds).mean()

print(f'Average session duration for SEIFUKU coding: {average_session_duration_seifuku_coding} seconds')
print(f'Average session duration for SEIFUKU managing: {average_session_duration_seifuku_managing} seconds')

# Calculate percentage of time spent on coding versus managing within SEIFUKU
total_seifuku_time = average_session_duration_seifuku * len(entries)
coding_time = average_session_duration_seifuku_coding * len(seifuku_coding_entries)
managing_time = average_session_duration_seifuku_managing * len(seifuku_managing_entries)

percentage_coding = (coding_time / total_seifuku_time) * 100
percentage_managing = (managing_time / total_seifuku_time) * 100

print(f'Percentage of time spent on coding within SEIFUKU: {percentage_coding}%')
print(f'Percentage of time spent on managing within SEIFUKU: {percentage_managing}%')

# Propose adjustments to alert thresholds if necessary
if average_session_duration_seifuku > 2 * average_session_duration_other_clients:
    print('Proposing adjustment to alert thresholds for SEIFUKU due to high average session duration.')
