"""Investigation: This script investigates the cause of the missing 'project_name' column in the dataframe and proposes modifications to the scripting approach or data processing pipeline to resolve the issue.
Generated: 20260305_175810 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

df = entries_to_dataframe(query_entries(days=30))
print(df.columns)
missing_columns = [col for col in ['project_name'] if col not in df.columns]
print(missing_columns)
if 'project_name' in missing_columns:
    print("'project_name' column is missing.")
else:
    print("'project_name' column exists.")