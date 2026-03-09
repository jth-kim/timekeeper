"""Investigation: This script investigates the task-level activities within SEIFUKU that contribute to its prolonged session durations and assesses their alignment with the Sovereign's objectives. It queries recent SEIFUKU entries, converts them to a DataFrame, calculates average session duration for SEIFUKU tasks, groups tasks by mean duration, and prints the top 5 tasks with the longest average durations.
Generated: 20260306_144046 UTC
"""


import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

def seifuku_task_level_activity_analysis():
    # Query recent SEIFUKU entries
    entries = query_entries(days=14, client='SEIFUKU')
    
    # Convert to DataFrame
    df = entries_to_dataframe(entries)
    
    # Calculate average session duration for SEIFUKU tasks
    avg_duration = df['duration_seconds'].mean()
    
    # Group tasks by mean duration
    task_durations = df.groupby('description')['duration_seconds'].mean().sort_values(ascending=False)
    
    # Print top 5 tasks with longest average durations
    print(task_durations.head(5))

seifuku_task_level_activity_analysis()
