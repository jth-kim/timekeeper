"""Investigation: This script investigates the underlying reasons for the high self-transition rate of SEIFUKU and assesses its impact on overall time allocation against target priorities by analyzing the transitions between sessions and identifying patterns or factors that contribute to this phenomenon.
Generated: 20260305_003724 UTC
"""

import pandas as pd
from supabase_helper import query_entries

df = pd.DataFrame(query_entries(days=30))
df['start'] = pd.to_datetime(df['start'])
seifuku_transitions = df[df['client_name'] == 'SEIFUKU']
self_transitions = seifuku_transitions[seifuku_transitions['previous_client'] == 'SEIFUKU']
print(self_transitions)