"""Investigation: This script analyzes the actual descriptive language in session entries (before the tag bracket) to identify if specific phrases correlate with project labels. Unlike previous investigations that focused on labels or gaps, it examines the Sovereign's own narrative language. The overlap analysis between STAR and SEIFUKU phrases is critical: if phrases like 'Self authoring' exclusively appear in mislabeled SEIFUKU sessions (while 'Time Series' appears only in STAR), it confirms intentional avoidance (not confusion). This directly tests the core mislabeling hypothesis from the journal with verifiable linguistic evidence.
Generated: 20260308_124612 UTC
"""

import pandas as pd
from supabase_helper import query_entries, entries_to_dataframe

# Fetch all entries (30 days)
entries = query_entries(days=30)
if not entries:
    print("No entries found for analysis")
    exit()

# Convert to DataFrame with proper duration handling
df = entries_to_dataframe(entries)

# Extract main description (before [tag])
def extract_main_desc(desc):
    if isinstance(desc, str) and '[' in desc:
        return desc.split('[')[0].strip()
    return desc if isinstance(desc, str) else ""

df['main_desc'] = df['description'].apply(extract_main_desc)

# Analyze per project type
projects = ['STAR', 'SEIFUKU', 'BBOY']
results = {}

for project in projects:
    project_df = df[df['project_name'] == project]
    if project_df.empty:
        continue
    
    # Count top phrases
    top_phrases = project_df['main_desc'].value_counts().head(3)
    results[project] = {
        phrase: count for phrase, count in top_phrases.items()
    }

# Print clear output
print("=== DESCRIPTION PHRASE DISTRIBUTION BY PROJECT ===")
print("\nTop 3 main description phrases for each project:")
for project, phrases in results.items():
    print(f"\n{project}:")
    for phrase, count in phrases.items():
        print(f"  - '{phrase}': {count} times")

# Check for overlap between STAR and SEIFUKU (key for mislabeling diagnosis)
star_phrases = set(results.get('STAR', {}).keys())
seifuku_phrases = set(results.get('SEIFUKU', {}).keys())
overlap = star_phrases & seifuku_phrases

print(f"\n\nSTAR and SEIFUKU phrases overlap: {len(overlap)} phrases")
if overlap:
    print("  Overlapping phrases:")
    for phrase in overlap:
        print(f"    - '{phrase}'")
else:
    print("  No overlapping phrases detected - suggests intentional labeling pattern")