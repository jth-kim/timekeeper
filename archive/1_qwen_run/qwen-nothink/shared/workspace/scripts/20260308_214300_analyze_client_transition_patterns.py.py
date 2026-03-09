"""Investigation: This investigates client transition patterns as a new operational rhythm metric. Previous gap analyses focused on session types, but client sequences reveal whether the Sovereign maintains continuity with specific clients (indicating deep work blocks) or switches frequently (suggesting fragmented focus). The 'same-client' count specifically identifies potential project continuity (e.g., back-to-back sessions with the same client), which correlates with strategic targets for focused work. This addresses a gap in our understanding of workflow sequencing beyond project types and tags, and directly informs scheduling interventions for strategic sessions.
Generated: 20260308_214300 UTC
"""

from supabase_helper import query_entries, entries_to_dataframe
from collections import defaultdict
import pandas as pd

# Query all entries (30 days) and convert to DataFrame
entries = query_entries(days=30)
df = entries_to_dataframe(entries)

df = df.sort_values('start')

transitions = defaultdict(int)
same_client_count = 0

# Process consecutive sessions
for i in range(len(df) - 1):
    prev_client = df.iloc[i]['client_name']
    next_client = df.iloc[i+1]['client_name']
    
    # Skip if either client is missing
    if pd.isna(prev_client) or pd.isna(next_client):
        continue
    
    # Count same-client transitions
    if prev_client == next_client:
        same_client_count += 1
    else:
        transitions[(prev_client, next_client)] += 1

# Print results
print("Client Transition Patterns (Consecutive Sessions)")
print("="*50)
print(f"Total consecutive session pairs: {len(transitions) + same_client_count}")
print(f"Same-client consecutive pairs: {same_client_count} ({same_client_count/len(transitions) * 100:.1f}%)")
print("\
Top 5 Transitions:")
for (prev, nxt), count in sorted(transitions.items(), key=lambda x: x[1], reverse=True)[:5]:
    print(f"{prev} → {nxt}: {count} times")

print("\
\
Note: Same-client patterns may indicate project continuity or scheduling blocks.")