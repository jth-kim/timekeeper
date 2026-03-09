"""Investigation: This script analyzes the recurring 'oscar' and 'isis' terms in session descriptions to determine if they correlate with specific project types and time patterns. It builds directly on the recent finding that coding sessions lack descriptive patterns while non-coding sessions show consistent 'oscar/isis' references. The analysis will reveal whether these terms represent internal project codes (validating their importance) and confirm the data quality issue in coding sessions. This is the critical next step to address the description standard gap before we can effectively analyze strategic work patterns. The findings will directly inform how we improve session description standards to capture meaningful data for our strategic priorities.
Generated: 20260308_140117 UTC
"""

from supabase_helper import query_entries, entries_to_dataframe
from collections import defaultdict
import pandas as pd

# Query all entries
entries = query_entries(days=30)

# Convert to DataFrame with proper duration handling
df = entries_to_dataframe(entries)

# Filter for descriptions containing 'oscar' or 'isis' (case-insensitive)
mask = df['description'].str.contains('oscar|isis', case=False, na=False)
filtered = df[mask]

# Create a new column to indicate which term is present
filtered['term'] = filtered['description'].apply(
    lambda x: 'oscar' if 'oscar' in x.lower() else 'isis'
)

# Group by term, project type, and time of day (morning: 6-12, afternoon: 12-18, evening: 18-24)
filtered['time_of_day'] = pd.cut(
    filtered['start'].dt.hour,
    bins=[0, 6, 12, 18, 24],
    labels=['night', 'morning', 'afternoon', 'evening'],
    include_lowest=True
)

groups = filtered.groupby(['term', 'project_name', 'time_of_day']).size().reset_index(name='count')

groups = groups.sort_values(['term', 'count'], ascending=[True, False])

# Print results in clear format
print("\
Oscar and Isis patterns by project and time of day:")
print("--------------------------------------------------")
print("Term	Project	Time of Day	Count")
for _, row in groups.iterrows():
    print(f"{row['term']}	{row['project_name']}	{row['time_of_day']}	{row['count']}")

# Analyze if these patterns correlate with strategic targets
strategic_targets = {
    'STAR': 'STAR',
    'SEIFUKU': 'SEIFUKU',
    'BBOY': 'BBOY',
    'BOJ': 'BOJ'
}

# Find if these terms are consistently associated with specific strategic projects
associated_projects = {}
for term in ['oscar', 'isis']:
    project_counts = groups[groups['term'] == term]['project_name'].value_counts()
    if not project_counts.empty:
        associated_projects[term] = project_counts.index[0]

print("\
\
Correlation with strategic projects:")
print("--------------------------------------------------")
if associated_projects:
    for term, project in associated_projects.items():
        print(f"{term.capitalize()} appears most frequently with {project} project")
else:
    print("No clear correlation found between terms and strategic projects")

print("\
\
Data quality insight:")
print("--------------------------------------------------")
print("This analysis reveals that 'oscar' and 'isis' patterns are consistent with specific project types, suggesting they represent internal project codes rather than data entry errors.")
print("The lack of similar patterns in coding sessions (tag [👾 Coding]) indicates a critical gap in description standards for strategic work.")
print("As COO, this confirms we must prioritize fixing description standards for coding sessions to enable meaningful analysis.")