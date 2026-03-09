"""Investigation: This script investigates the factors contributing to the high average session duration for SEIFUKU compared to other clients and how this impacts the Sovereign's productivity and goal achievement. It calculates the average session durations for SEIFUKU, STAR, and BBOY, and then investigates the factors contributing to the longer average session duration for SEIFUKU by calculating the percentage of time spent on coding versus managing within SEIFUKU. Finally, it proposes adjustments to alert thresholds if necessary based on the total time spent on each client.
Generated: 20260305_142343 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data for SEIFUKU
entries = query_entries(days=14, client='SEIFUKU')

# Convert entries to a DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate average session duration for SEIFUKU
average_duration_seifuku = df['duration_seconds'].mean()

# Query recent time-tracking data for other clients (STAR and BBOY)
entries_star = query_entries(days=14, client='STAR')
entries_bboy = query_entries(days=14, client='BBOY')

# Convert entries to DataFrames with proper types
df_star = entries_to_dataframe(entries_star)
df_bboy = entries_to_dataframe(entries_bboy)

# Calculate average session durations for STAR and BBOY
average_duration_star = df_star['duration_seconds'].mean()
average_duration_bboy = df_bboy['duration_seconds'].mean()

# Print findings
print(f'Average session duration for SEIFUKU: {average_duration_seifuku} seconds')
print(f'Average session duration for STAR: {average_duration_star} seconds')
print(f'Average session duration for BBOY: {average_duration_bboy} seconds')

# Investigate factors contributing to the longer average session duration for SEIFUKU
print('Investigating factors contributing to the longer average session duration for SEIFUKU...')

# Calculate the percentage of time spent on coding versus managing within SEIFUKU
coding_time_seifuku = df[df['project_name'] == 'Artemis']['duration_seconds'].sum()
managing_time_seifuku = df[df['project_name'] != 'Artemis']['duration_seconds'].sum()
percentage_coding_seifuku = (coding_time_seifuku / (coding_time_seifuku + managing_time_seifuku)) * 100

print(f'Percentage of time spent on coding within SEIFUKU: {percentage_coding_seifuku}%')

# Propose adjustments to alert thresholds if necessary
print('Proposing adjustments to alert thresholds if necessary...')

# Calculate the total time spent on SEIFUKU, STAR, and BBOY
total_time_seifuku = df['duration_seconds'].sum()
total_time_star = df_star['duration_seconds'].sum()
total_time_bboy = df_bboy['duration_seconds'].sum()

# Check if the time allocation is within the target ranges
if total_time_seifuku > 0.15 * (total_time_seifuku + total_time_star + total_time_bboy):
    print('Adjusting alert thresholds to reflect the increased time allocation for SEIFUKU...')
else:
    print('No adjustments needed.')
