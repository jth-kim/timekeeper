"""Investigation: This script investigates how coding sessions (tag [👾 Coding]) vary in duration by time of day (morning, afternoon, evening) and project type (STAR vs SEIFUKU). It builds on the previous failed attempt but fixes the syntax error and provides a granular analysis. The analysis is critical because it addresses the data quality issue identified in earlier work (coding sessions lack descriptive patterns), allowing us to determine if time of day correlates with session depth and whether strategic priorities (STAR/SEIFUKU) are being executed during optimal periods. This directly supports our strategic target of maximizing focus during high-impact sessions, and the results will inform whether the Sovereign should schedule coding sessions during specific time blocks for better outcomes.
Generated: 20260308_142718 UTC
"""

from supabase_helper import query_entries, entries_to_dataframe
from supabase_helper import parse_duration_seconds
import pandas as pd
import numpy as np
from datetime import datetime

# Query all entries from the past 30 days
entries = query_entries(days=30)

def categorize_time_of_day(start_time):
    # Convert to datetime object if it's a string
    if isinstance(start_time, str):
        start_time = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
    hour = start_time.hour
    if 6 <= hour < 12:
        return 'morning'
    elif 12 <= hour < 18:
        return 'afternoon'
    elif 18 <= hour < 24:
        return 'evening'
    else:
        return 'night'

# Convert entries to DataFrame with proper duration handling
df = entries_to_dataframe(entries)

df['time_of_day'] = df['start'].apply(categorize_time_of_day)

def get_project_type(tags):
    if 'STAR' in tags:
        return 'STAR'
    elif 'SEIFUKU' in tags:
        return 'SEIFUKU'
    else:
        return 'other'

df['project_type'] = df['tags'].apply(get_project_type)

def analyze_coding_sessions(df):
    coding_sessions = df[df['tags'].apply(lambda x: '👾 Coding' in x if isinstance(x, list) else False)]
    
    if coding_sessions.empty:
        return "No coding sessions found in the data."

    # Calculate average duration by time of day
    grouped = coding_sessions.groupby(['time_of_day', 'project_type'])['duration_minutes'].mean().reset_index()
    grouped = grouped.round(1)
    
    # Format the results for printing
    results = []
    for _, row in grouped.iterrows():
        results.append(f"{row['project_type']} {row['time_of_day']} sessions: {row['duration_minutes']} minutes")
    
    return "\
".join(results)

# Run the analysis
print("Coding session duration patterns by time of day and project type:")
print(analyze_coding_sessions(df))