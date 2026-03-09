"""Investigation: This script calculates the actual hour totals for each client over the last week and compares these totals to the target allocations, providing insights into potential imbalances in time allocation.
Generated: 20260306_210448 UTC
"""


from supabase_helper import query_entries, entries_to_dataframe

# Query recent time-tracking data
entries = query_entries(days=7)

# Convert entries to a pandas DataFrame with proper types
df = entries_to_dataframe(entries)

# Calculate total hours for each client
client_hours = df.groupby('client_name')['duration_seconds'].sum() / 3600

# Print the results in a clear format
print(client_hours)
