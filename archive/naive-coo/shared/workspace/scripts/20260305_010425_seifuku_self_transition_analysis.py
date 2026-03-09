"""Investigation: This script investigates the high self-transition rate of SEIFUKU by analyzing the transitions between sessions and identifying patterns or factors that contribute to this phenomenon. It queries the time-tracking data for the last 30 days, filters the entries for SEIFUKU, and then identifies the instances where SEIFUKU is followed by itself.
Generated: 20260305_010425 UTC
"""

import pandas as pd
from supabase_helper import query_entries

df = pd.DataFrame(query_entries(days=30))
# Ensure 'start' column is datetime type for analysis
df['start'] = pd.to_datetime(df['start'])

df_seifuku = df[df['client_name'] == 'SEIFUKU']
seifuku_transitions = df_seifuku[(df_seifuku['previous_client'] == 'SEIFUKU')]

print("Number of SEIFUKU self-transitions:", len(seifuku_transitions))
print("Proportion of SEIFUKU sessions that are self-transitions:", len(seifuku_transitions) / len(df_seifuku))