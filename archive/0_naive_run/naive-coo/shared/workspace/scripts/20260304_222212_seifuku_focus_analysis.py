"""Investigation: This script investigates the total time spent on SEIFUKU tasks over the last 30 days to understand the extent of focus on this client and potential implications for long-term goals.
Generated: 20260304_222212 UTC
"""

import pandas as pd
from supabase_helper import query_entries

df = pd.DataFrame(query_entries(days=30))
seifuku_entries = df[df['client_name'] == 'SEIFUKU']
total_seifuku_time = seifuku_entries['duration'].sum()
print(f'Total time spent on SEIFUKU in the last 30 days: {total_seifuku_time}')