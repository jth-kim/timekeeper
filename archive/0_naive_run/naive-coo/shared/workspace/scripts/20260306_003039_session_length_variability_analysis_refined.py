"""Investigation: This script calculates the average session duration for each client over the last two weeks and investigates factors contributing to variability in session lengths, providing insights into potential imbalances or patterns that could inform adjustments to priorities or alert thresholds.
Generated: 20260306_003039 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

def session_length_variability_analysis():
    # Query recent entries
    entries = query_entries(days=14)
    df = entries_to_dataframe(entries)
    
    # Calculate average session duration for each client
    avg_session_durations = df.groupby('client_name')['duration_seconds'].mean().reset_index()
    print(avg_session_durations)
    
    # Investigate factors contributing to variability
    for client in avg_session_durations['client_name'].unique():
        client_df = df[df['client_name'] == client]
        print(f'Client: {client}')
        print(client_df.describe())
        print()

session_length_variability_analysis()