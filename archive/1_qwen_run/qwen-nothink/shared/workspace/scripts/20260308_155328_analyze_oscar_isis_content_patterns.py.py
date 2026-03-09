"""Investigation: This script analyzes the actual content of session descriptions containing 'oscar' or 'isis' (case-insensitive), identifying specific phrases and project types associated with these patterns. It moves beyond simple frequency counts to extract 3-word phrase patterns and determines if these patterns align with strategic project types (SEIFUKU/STAR). This addresses the critical data quality issue identified in my last investigation (coding sessions lack descriptive patterns) by examining the meaning behind the non-coding session patterns. The findings will determine whether 'oscar' and 'isis' represent meaningful strategic work patterns or data entry artifacts, directly informing how we should structure session descriptions to capture strategic relevance. This is the first investigation to analyze the *content* of descriptions rather than just the presence of certain terms.
Generated: 20260308_155328 UTC
"""

from supabase_helper import query_entries, entries_to_dataframe
from collections import Counter
import re

# Get all entries
entries = query_entries(days=30)
if not entries:
    print("No entries found")
    exit()

df = entries_to_dataframe(entries)

df['description_lower'] = df['description'].str.lower()

# Filter for sessions containing 'oscar' or 'isis' (case-insensitive)
oscar_isis_entries = df[df['description_lower'].str.contains(r'\boscar\b|\bisis\b', regex=True, na=False)]

def analyze_patterns(df):
    if df.empty:
        return "No entries match the pattern"

    # Group by project type and count occurrences
    project_counts = df['project_name'].value_counts()
    project_patterns = {}

    # For each project, analyze the most common description patterns
    for project in project_counts.index:
        project_df = df[df['project_name'] == project]
        descriptions = project_df['description_lower'].tolist()
        
        # Extract common phrases (3-word sequences)
        phrases = []
        for desc in descriptions:
            words = re.findall(r'\b\w+\b', desc)
            for i in range(len(words) - 2):
                phrases.append(' '.join(words[i:i+3]))
        
        phrase_counts = Counter(phrases)
        top_phrases = phrase_counts.most_common(3)
        
        project_patterns[project] = {
            'count': project_counts[project],
            'top_phrases': top_phrases
        }
    
    return project_patterns

# Analyze patterns
patterns = analyze_patterns(oscar_isis_entries)

# Output results
print("SESSION DESCRIPTION PATTERNS WITH 'OSCAR' OR 'ISIS' (", len(oscar_isis_entries), "entries)")
print("\
" + "-"*50 + "\
")

for project, data in patterns.items():
    print(f"Project: {project}")
    print(f"  Count: {data['count']}")
    print("  Top 3 descriptive phrases:")
    for phrase, count in data['top_phrases']:
        print(f"    - {phrase} ({count} occurrences)")
    print()

# Check if these patterns align with strategic targets
strategic_projects = ['SEIFUKU', 'STAR']
strategic_alignments = {}
for project in strategic_projects:
    if project in patterns:
        strategic_alignments[project] = patterns[project]

if strategic_alignments:
    print("\
STRATEGIC ALIGNMENT CHECK:")
    print("-"*50 + "\
")
    for project, data in strategic_alignments.items():
        print(f"{project} sessions with 'oscar'/'isis' ({data['count']} sessions)")
        print(f"  Top phrases: {', '.join([p[0] for p in data['top_phrases']])}")
        print()
else:
    print("\
No strategic project patterns found in 'oscar'/'isis' sessions")