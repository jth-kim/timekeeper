"""Investigation: This script investigates the weekly time distribution trends across clients over an extended period of 60 days and compares these trends to the target allocations, providing a broader perspective on time allocation patterns.
Generated: 20260306_090452 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

def calculate_weekly_time_distribution(entries):
    # Convert entries to DataFrame
    df = entries_to_dataframe(entries)
    
    # Ensure 'start' column is datetime
    df['start'] = pd.to_datetime(df['start'])
    
    # Extract week number from 'start' date
    df['week'] = df['start'].dt.isocalendar().week
    
    # Group by client and week, sum duration_seconds
    weekly_distribution = df.groupby(['client_name', 'week'])['duration_seconds'].sum().reset_index()
    
    return weekly_distribution

# Query entries for the last 60 days
entries = query_entries(days=60)

# Calculate weekly time distribution
weekly_distribution = calculate_weekly_time_distribution(entries)

# Print results
print(weekly_distribution)
