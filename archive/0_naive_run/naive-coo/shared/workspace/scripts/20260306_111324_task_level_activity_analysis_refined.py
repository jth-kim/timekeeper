"""Investigation: This script investigates the technical issue with the task_level_activity_analysis_across_clients script and refines the investigation strategy to prioritize detailed task analyses within each client. It queries recent time-tracking data, converts it into a pandas DataFrame, filters by client and project, calculates mean duration for each task, and prints the results in a clear format.
Generated: 20260306_111324 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

def refine_task_level_activity_analysis():
    # Query recent time-tracking data for the last 14 days
    entries = query_entries(days=14)
    
    # Convert to DataFrame and ensure 'duration' column is numeric
    df = entries_to_dataframe(entries)
    
    # Filter by client and project, then calculate mean duration for each task
    seifuku_tasks = df[df['client_name'] == 'SEIFUKU'].groupby('project_name')['duration_seconds'].mean()
    star_tasks = df[df['client_name'] == 'STAR'].groupby('project_name')['duration_seconds'].mean()
    bboy_tasks = df[df['client_name'] == 'BBOY'].groupby('project_name')['duration_seconds'].mean()
    
    # Print results in a clear format
    print("SEIFUKU Tasks:")
    print(seifuku_tasks)
    print("\
STAR Tasks:")
    print(star_tasks)
    print("\
BBOY Tasks:")
    print(bboy_tasks)
    
    # Save the script to /data/workspace/tools/ for future use
    with open('/data/workspace/tools/task_level_activity_analysis_refined.py', 'w') as file:
        file.write('import pandas as pd\
from supabase_helper import query_entries, entries_to_dataframe\
\
def refine_task_level_activity_analysis():\
    # Query recent time-tracking data for the last 14 days\
    entries = query_entries(days=14)\
    \
    # Convert to DataFrame and ensure \'duration\' column is numeric\
    df = entries_to_dataframe(entries)\
    \
    # Filter by client and project, then calculate mean duration for each task\
    seifuku_tasks = df[df[\'client_name\'] == \'SEIFUKU\'].groupby(\'project_name\')[\'duration_seconds\'].mean()\
    star_tasks = df[df[\'client_name\'] == \'STAR\'].groupby(\'project_name\')[\'duration_seconds\'].mean()\
    bboy_tasks = df[df[\'client_name\'] == \'BBOY\'].groupby(\'project_name\')[\'duration_seconds\'].mean()\
    \
    # Print results in a clear format\
    print("SEIFUKU Tasks:")\
    print(seifuku_tasks)\
    print("\\
STAR Tasks:")\
    print(star_tasks)\
    print("\\
BBOY Tasks:")\
    print(bboy_tasks)\
\
    # Execute the function to test it
refine_task_level_activity_analysis()