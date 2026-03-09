"""Investigation: This script investigates how to convert the 'start' column in the dataframe to a datetime format. The conversion is necessary for grouping by time frequencies and calculating weekly time distribution trends across clients.
Generated: 20260305_055513 UTC
"""


import pandas as pd
from supabase_helper import query_entries

# Query recent entries
entries = query_entries(days=30)

# Convert to DataFrame
df = pd.DataFrame(entries)

# Convert 'start' column to datetime format
df['start'] = pd.to_datetime(df['start'])

# Print the first few rows of the dataframe to verify conversion
print(df.head())
