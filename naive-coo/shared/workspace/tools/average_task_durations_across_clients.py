"""Investigation: This script calculates the average task durations within each client over the last week and compares these averages across clients, providing insights into potential imbalances or patterns that could inform adjustments to priorities or alert thresholds.
Generated: 20260305_100601 UTC
"""


from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data
entries = query_entries(days=7)

# Convert to DataFrame with proper types
df = entries_to_dataframe(entries)

# Group by client and calculate average task duration
average_durations = df.groupby('client_name')['duration_seconds'].mean().reset_index()

# Print the results in a readable format
print("Average Task Durations Across Clients:")
print(average_durations.to_string(index=False))
