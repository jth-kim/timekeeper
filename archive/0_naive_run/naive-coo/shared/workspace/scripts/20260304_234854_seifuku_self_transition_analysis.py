"""Investigation: This script investigates the underlying reasons for the high self-transition rate of SEIFUKU by analyzing the transitions between sessions and identifying patterns or factors that contribute to this phenomenon. It queries the time-tracking data for the last 30 days, filters the entries for SEIFUKU, and then identifies the instances where SEIFUKU is followed by itself. The output will provide insights into the specific activities or tasks within SEIFUKU that lead to high self-transitions and how these impact the overall time allocation against target priorities.
Generated: 20260304_234854 UTC
"""

import pandas as pd
from supabase_helper import query_entries

df = query_entries(days=30)
seifuku_transitions = df[df['client_name'] == 'SEIFUKU']
self_transitions = seifuku_transitions[seifuku_transitions['previous_client'] == 'SEIFUKU']
print(self_transitions)