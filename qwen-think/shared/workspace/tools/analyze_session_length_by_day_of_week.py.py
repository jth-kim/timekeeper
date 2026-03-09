"""Investigation: This investigation analyzes session length patterns by day of week to identify normal work rhythms and distinguish between expected patterns (e.g., longer sessions on weekends) and potential disengagement periods. The results will help determine if the observed 42h gap between sessions is part of a normal weekend rest pattern or indicates disengagement. This is a new angle that directly impacts the Sovereign's work rhythm and time management awareness, building on previous gap analysis but adding temporal context to distinguish between intentional rest (weekends) and operational risk (weekdays). It avoids repeating previous investigations by focusing on day-of-week patterns rather than hour-of-day patterns.
Generated: 20260308_140731 UTC
"""

from supabase_helper import query_entries, entries_to_dataframe
import pandas as pd

def main():
    # Get all entries from the last 30 days
    entries = query_entries(days=30)
    
    # Convert entries to DataFrame with proper duration columns
    df = entries_to_dataframe(entries)
    
    # Extract day of week (0=Monday, 6=Sunday)
    df['day_of_week'] = df['start'].dt.weekday
    
    # Create a mapping from number to day name
    day_names = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
    
    # Group by day of week and calculate average duration in minutes
    daily_avg = df.groupby('day_of_week').agg(
        avg_duration_minutes=('duration_minutes', 'mean'),
        count=('duration_minutes', 'count')
    ).reset_index()
    
    # Map day numbers to day names
    daily_avg['day_name'] = daily_avg['day_of_week'].map(day_names)
    
    # Sort by day of week
    daily_avg = daily_avg.sort_values('day_of_week')
    
    # Print results
    print("Session Length by Day of Week (average in minutes):")
    print("Day of Week | Average Session Length | Number of Sessions")
    print("-------------------------------------------------------")
    for _, row in daily_avg.iterrows():
        print(f"{row['day_name']:<12} | {row['avg_duration_minutes']:20.2f} | {row['count']:20d}")

if __name__ == "__main__":
    main()