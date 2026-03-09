"""Investigation: This script identifies the most common sequences between session types (e.g., BBOY followed by SEIFUKU) across all project types. It reveals workflow patterns that could inform scheduling strategies and validate whether the current project type sequencing aligns with strategic priorities. This is a new angle that hasn't been explored in previous investigations, moving beyond duration analysis to examine sequence patterns in the data. It builds on our recent understanding of session types while opening a new dimension of analysis for operational optimization.
Generated: 20260308_150812 UTC
"""

from supabase_helper import query_entries, entries_to_dataframe
import pandas as pd
from collections import defaultdict

# Get all entries from the last 30 days
entries = query_entries(days=30)
df = entries_to_dataframe(entries)

df['next_session_type'] = df['project_name'].shift(-1)
df = df[:-1]  # Remove last entry which has no next session

# Group by current session type and next session type
t = df.groupby(['project_name', 'next_session_type']).size().reset_index(name='count')
t = t.sort_values('count', ascending=False)
t['percentage'] = (t['count'] / t['count'].sum()) * 100

top_transitions = t.head(10)

counts = df[['project_name', 'next_session_type']].value_counts().to_dict()

print("Most common session transitions (top 10):")
for i, (current, next) in enumerate(counts.keys(), 1):
    count = counts[(current, next)]
    percentage = (count / sum(counts.values())) * 100
    print(f"{i}. {current} → {next}: {count} occurrences ({percentage:.2f}%)")

print(f"\
Total transitions analyzed: {len(df)}")
print(f"Most common transition: {top_transitions.iloc[0]['project_name']} → {top_transitions.iloc[0]['next_session_type']} ({top_transitions.iloc[0]['count']} occurrences)")