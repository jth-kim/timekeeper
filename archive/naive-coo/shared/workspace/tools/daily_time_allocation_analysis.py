"""Investigation: This script adjusts the dataframe to ensure the 'start' column is of the correct data type (datetime) for the grouper function, allowing us to successfully analyze daily time allocation patterns across different clients over the past two weeks.
Generated: 20260304_223540 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query entries from the last two weeks
entries = query_entries(days=14)

# Convert the 'start' column to datetime type if it's not already
df = pd.DataFrame(entries)
df['start'] = pd.to_datetime(df['start'])

# Ensure the dataframe is sorted by the 'start' column
df.sort_values(by='start', inplace=True)

# Set the 'start' column as the index for easier grouping
df.set_index('start', inplace=True)

# Now, use the grouper function to analyze daily time allocation patterns
daily_client_time = df.groupby([pd.Grouper(freq='D')]).sum()

print(daily_client_time)
