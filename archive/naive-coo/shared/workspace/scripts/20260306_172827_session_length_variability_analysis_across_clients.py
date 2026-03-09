"""Investigation: This script investigates the factors contributing to the session length variability across clients and assesses their impact on overall time allocation. By analyzing recent time-tracking data, it calculates mean session lengths for each client and provides insights into potential imbalances or patterns that could inform adjustments to priorities or alert thresholds.
Generated: 20260306_172827 UTC
"""


import pandas as pd
from supabase_helper import query_entries, parse_duration_seconds

# Query recent entries (e.g., last 14 days)
entries = query_entries(days=14)

# Convert to DataFrame with proper types
df = pd.DataFrame(entries)

# Calculate session lengths in seconds
df['duration_seconds'] = df['duration'].apply(parse_duration_seconds)

# Group by client and calculate mean session length
mean_session_lengths = df.groupby('client_name')['duration_seconds'].mean()

# Print results
print(mean_session_lengths)
