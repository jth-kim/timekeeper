"""Investigation: This script investigates the factors contributing to session length variability across clients over 14 days by calculating mean, min, max, and standard deviation of session lengths for each client.
Generated: 20260306_060402 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

df = entries_to_dataframe(query_entries(days=14))
# Calculate session length in seconds for each entry and store it in a new column 'session_length_seconds'
df['session_length_seconds'] = df['duration'].apply(lambda x: parse_duration_seconds(x))
# Group the data by client_name and calculate mean, min, max, and standard deviation of session lengths
client_session_lengths = df.groupby('client_name')['session_length_seconds'].agg(['mean', 'min', 'max', 'std'])
print(client_session_lengths)