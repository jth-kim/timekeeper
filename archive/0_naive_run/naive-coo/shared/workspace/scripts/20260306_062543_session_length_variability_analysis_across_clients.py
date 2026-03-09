"""Investigation: This script investigates the factors contributing to the significant variability in session lengths across different clients and projects over the last 14 days. It calculates the mean session length for each client and project, providing insights into potential imbalances or patterns that could inform adjustments to priorities or alert thresholds.
Generated: 20260306_062543 UTC
"""


import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds

# Query entries for the last 14 days
entries = query_entries(days=14)

# Convert to DataFrame with proper duration handling
df = entries_to_dataframe(entries)

# Calculate mean session length for each client and project
mean_session_lengths = df.groupby(['client_name', 'project_name'])['duration_seconds'].mean().reset_index()

# Print the results
print(mean_session_lengths)
