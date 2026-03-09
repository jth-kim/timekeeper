"""Investigation: This investigation moves beyond pattern recognition to analyze whether the 'oscar/isis' descriptive pattern (observed in non-coding sessions) aligns with strategic work allocation targets. By mapping these sessions to project types (STAR/SEIFUKU vs BBOY/BOJ), we determine if the pattern is actually tied to strategic work (as intended) or misaligned with priorities. The findings directly address the data quality issue (coding sessions lack patterns) while revealing whether non-coding session patterns are meaningful. This is the first investigation to connect descriptive patterns to strategic allocation targets, moving from observation to strategic relevance.
Generated: 20260308_165123 UTC
"""

from supabase_helper import query_entries, entries_to_dataframe
from collections import Counter
import pandas as pd

# Get all entries (last 30 days)
entries = query_entries(days=30)
if not entries:
    print('No entries found')
    exit()

df = entries_to_dataframe(entries)

df['description_lower'] = df['description'].str.lower() if df['description'].notna().any() else pd.Series([''] * len(df))

code_words = ['oscar', 'isis']
mask = df['description_lower'].apply(lambda x: any(word in x for word in code_words))

filtered = df[mask]

if filtered.empty:
    print('No sessions found containing oscar/isis in descriptions')
else:
    # Get project type distribution
    project_counts = filtered['project_name'].value_counts().to_dict()
    total = len(filtered)
    
    # Calculate percentages
    percentages = {k: (v / total) * 100 for k, v in project_counts.items()}
    
    # Format output
    print(f'Found {total} sessions containing "oscar" or "isis" in descriptions (case-insensitive)')
    print('\
Distribution by project type:')
    for project, count in project_counts.items():
        print(f'  - {project}: {count} ({percentages[project]:.1f}%)')
    
    # Check against strategic targets
    strategic_targets = {'STAR': 0.55, 'SEIFUKU': 0.15}
    strategic_total = sum(project_counts.get(p, 0) for p in strategic_targets.keys())
    strategic_pct = (strategic_total / total) * 100
    
    print(f'\
Strategic project type (STAR/SEIFUKU) share: {strategic_pct:.1f}%')
    print(f'\
Strategic allocation target: {sum(strategic_targets.values())*100:.0f}%')
    print(f'\
Discrepancy: {strategic_pct:.1f}% vs target {sum(strategic_targets.values())*100:.0f}%')
    
    # Check if distribution aligns with targets
    if strategic_pct > 60:
        print('\
⚠️ WARNING: Strategic project type share significantly exceeds target (over 60%)')
    elif strategic_pct < 40:
        print('\
⚠️ WARNING: Strategic project type share significantly below target (under 40%)')
    else:
        print('\
✅ Strategic project type share within expected range')