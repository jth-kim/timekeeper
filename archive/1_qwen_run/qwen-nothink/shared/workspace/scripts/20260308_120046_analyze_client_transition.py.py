"""Investigation: This script analyzes the sequence of client transitions to uncover work context patterns. It identifies the most common transitions between client types (e.g., SEIFUKU → STAR) which reveals whether context switching is intentional (e.g., after deep work) or chaotic. This is the first investigation to examine client sequence rather than project types or tags, addressing a gap in understanding work flow dynamics. The top transitions will indicate if the Sovereign systematically moves between work types (e.g., deep work to client meetings) or switches haphazardly, which directly impacts energy management and focus preservation.
Generated: 20260308_120046 UTC
"""

from supabase_helper import query_entries, entries_to_dataframe
import pandas as pd

def main():
    # Get last 30 days of entries
    entries = query_entries(days=30)
    df = entries_to_dataframe(entries)
    
    # Sort by start time to get chronological order
    df = df.sort_values('start')
    
    # Create next_client column (shift to get next session's client)
    df['next_client'] = df['client_name'].shift(-1)
    
    # Filter out last session (no next session)
    df = df.dropna(subset=['next_client'])
    
    # Count transitions between clients
    transitions = df.groupby(['client_name', 'next_client']).size().reset_index(name='count')
    transitions = transitions.sort_values('count', ascending=False)
    
    # Print top 10 transitions
    print("Top 10 Client Transitions (Most Frequent First)")
    print("========================================")
    for i, row in transitions.head(10).iterrows():
        print(f"{row['client_name']} → {row['next_client']}: {row['count']} times")
    
    # Additional context: Calculate transition density
    total_transitions = len(df)
    unique_transitions = len(transitions)
    print(f"\
Total transitions: {total_transitions} | Unique transition paths: {unique_transitions}")
    print(f"Average transitions per session: {total_transitions/len(df):.2f}")

if __name__ == '__main__':
    main()