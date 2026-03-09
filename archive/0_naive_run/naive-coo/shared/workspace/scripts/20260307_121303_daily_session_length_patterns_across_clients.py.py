"""Investigation: This script investigates the daily patterns of session lengths for each client over the last 14 days, providing insights into how productivity varies across different days and clients.
Generated: 20260307_121303 UTC
"""


from supabase_helper import query_entries, entries_to_dataframe
import pandas as pd

def calculate_daily_session_lengths(entries):
    df = entries_to_dataframe(entries)
    df['date'] = df['start'].dt.date
    daily_session_lengths = df.groupby(['client_name', 'date'])['duration_seconds'].mean().reset_index()
    return daily_session_lengths

def main():
    entries = query_entries(days=14)
    daily_session_lengths = calculate_daily_session_lengths(entries)
    print(daily_session_lengths)

if __name__ == '__main__':
    main()
