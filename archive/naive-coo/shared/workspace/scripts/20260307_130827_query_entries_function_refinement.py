"""Investigation: This script aims to refine the 'query_entries' function by adding error handling and support for client-specific queries. It tests this refinement with a specific client, SEIFUKU, over the last 14 days.
Generated: 20260307_130827 UTC
"""


import json
from supabase_helper import query_entries

def refined_query_entries(days, client=None):
    if client:
        try:
            # Assuming 'client' is a valid column in the entries table
            entries = query_entries(days=days)
            filtered_entries = [entry for entry in entries if entry['client_name'] == client]
            return filtered_entries
        except Exception as e:
            print(f"Error refining query: {e}")
            return []
    else:
        return query_entries(days=days)

# Test the refined function
print(refined_query_entries(14, client='SEIFUKU'))
