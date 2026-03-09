"""Investigation: This investigation addresses the data quality issue we identified (coding sessions lack descriptive patterns) by exploring the correlation between 'oscar'/'isis' references in descriptions and client names. It's a new angle that builds on our previous discovery of these terms in non-coding sessions, but moves beyond just pattern recognition to examine their relationship with specific clients. The findings will help us determine if these terms represent client-specific projects or internal naming conventions, which directly informs how we should improve session description standards. This is the first investigation to connect description patterns with client names, providing actionable insights for data quality improvements.
Generated: 20260308_162056 UTC
"""

from supabase_helper import query_entries, entries_to_dataframe
import pandas as pd
import numpy as np

# Query all entries for the last 30 days
entries = query_entries(days=30)
if not entries:
    print("No entries found for analysis.")
    exit()

# Convert to DataFrame with proper duration handling
df = entries_to_dataframe(entries)

df['description_lower'] = df['description'].str.lower()

# Filter for sessions containing 'oscar' or 'isis' in description
oscar_isis_mask = df['description_lower'].str.contains(r'oscar|isis', na=False)
oscar_isis_df = df[oscar_isis_mask]

# Calculate statistics for sessions with 'oscar'/'isis'
if not oscar_isis_df.empty:
    oscar_isis_stats = {
        'total_sessions': len(oscar_isis_df),
        'avg_duration_minutes': oscar_isis_df['duration_minutes'].mean(),
        'client_distribution': oscar_isis_df['client_name'].value_counts().to_dict()
    }
else:
    oscar_isis_stats = {'total_sessions': 0}

# Calculate statistics for all other sessions
other_sessions_df = df[~oscar_isis_mask]
if not other_sessions_df.empty:
    other_stats = {
        'total_sessions': len(other_sessions_df),
        'avg_duration_minutes': other_sessions_df['duration_minutes'].mean()
    }
else:
    other_stats = {'total_sessions': 0}

# Print findings
print("=== Sessions containing 'oscar' or 'isis' in descriptions ===")
if oscar_isis_stats['total_sessions'] > 0:
    print(f"- Total sessions: {oscar_isis_stats['total_sessions']}")
    print(f"- Average duration: {oscar_isis_stats['avg_duration_minutes']:.1f} minutes")
    print("- Client distribution:")
    for client, count in oscar_isis_stats['client_distribution'].items():
        print(f"  • {client}: {count} sessions")
else:
    print("- No sessions containing 'oscar' or 'isis' found.")

print("\
=== Comparison with other sessions ===")
if other_stats['total_sessions'] > 0:
    print(f"- Total sessions: {other_stats['total_sessions']}")
    print(f"- Average duration: {other_stats['avg_duration_minutes']:.1f} minutes")
    print(f"- Difference: {oscar_isis_stats['avg_duration_minutes'] - other_stats['avg_duration_minutes']:.1f} minutes")
else:
    print("- No other sessions found for comparison.")