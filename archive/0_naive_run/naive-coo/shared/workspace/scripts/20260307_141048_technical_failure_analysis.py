"""Investigation: This script investigates the underlying causes of repeated technical failures in scripts designed to analyze task-level activity patterns. It attempts to run each failed script and stores any error messages that occur during execution. By analyzing these error messages, we can identify common issues and systematically address them to ensure reliable data processing and analysis.
Generated: 20260307_141048 UTC
"""


import sys
from supabase_helper import query_entries

def analyze_script_failures():
    # List of recent script failures
    failed_scripts = [
        'seifuku_task_level_activity_variability_analysis_r.py',
        'untracked_time_variability_analysis_across_clients.py',
        'seifuku_session_duration_analysis.py'
    ]

    # Initialize a dictionary to store error messages
    error_messages = {}

    for script in failed_scripts:
        try:
            # Attempt to run the script
            exec(open(script).read())
        except Exception as e:
            # Store the error message if an exception occurs
            error_messages[script] = str(e)

    return error_messages

# Execute the function and print the results
error_messages = analyze_script_failures()
for script, error in error_messages.items():
    print(f'Script: {script}, Error: {error}')
