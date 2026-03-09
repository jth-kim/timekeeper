"""Investigation: This script analyzes the sequence of client projects to identify habitual transitions (e.g., SEIFUKU followed by STAR). It's the first investigation focused on workflow patterns after two failed attempts on session gaps and length. The Sovereign's recent data shows heavy coding sessions (SEIFUKU), so we're testing whether transitions reveal intentional workflow rhythms. If SEIFUKU consistently leads to STAR, it suggests structured focus shifts; if it leads to BBOY (training), it might indicate energy management patterns. This insight is critical for understanding operational rhythm beyond isolated metrics.
Generated: 20260308_111657 UTC
"""

from supabase_helper import query_entries, entries_to_dataframe
import pandas as pd

# Get all entries from last 7 days
entries = query_entries(days=7)
if len(entries) < 2:
    print(f"Not enough sessions (only {len(entries)} found) to analyze transitions. Requires at least 2 consecutive sessions.")
    exit()

df = entries_to_dataframe(entries)
df = df.sort_values('start').reset_index(drop=True)

# Track transitions between client_name
transitions = {}

for i in range(len(df) - 1):
    from_client = df.iloc[i]['client_name']
    to_client = df.iloc[i+1]['client_name']
    
    if from_client not in transitions:
        transitions[from_client] = {}
    if to_client not in transitions[from_client]:
        transitions[from_client][to_client] = 0
    transitions[from_client][to_client] += 1

# Print results in readable format
print("\
Client Transition Matrix (last 7 days, consecutive sessions)")
print("From\	To\	Count")

# Sort transitions for readability
sorted_from = sorted(transitions.keys())
for from_client in sorted_from:
    sorted_to = sorted(transitions[from_client].keys())
    for to_client in sorted_to:
        count = transitions[from_client][to_client]
        print(f"{from_client}\	{to_client}\	{count}")

# Additional insight if transitions exist
if transitions:
    most_common = max(transitions, key=lambda x: sum(transitions[x].values()))
    print(f"\
Most frequent starting project: {most_common}")