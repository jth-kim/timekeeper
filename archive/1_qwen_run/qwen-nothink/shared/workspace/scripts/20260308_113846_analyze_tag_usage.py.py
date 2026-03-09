"""Investigation: This script analyzes session count and average duration per tag, correcting the previous syntax error that caused false 'nan' results. It properly handles the 'tags' field as a list, explodes multi-tag entries, and computes meaningful metrics. The output reveals actual activity patterns (e.g., how much time is spent on coding vs. training sessions), validating whether the tagging system aligns with observed behavior. This directly addresses the agenda item and moves beyond superficial project-type analysis to uncover true activity allocation.
Generated: 20260308_113846 UTC
"""

from supabase_helper import query_entries, entries_to_dataframe
import pandas as pd

df = entries_to_dataframe(query_entries(days=30))

# Handle potential non-list tags by converting to list
if not df.empty:
    df['tags'] = df['tags'].apply(lambda x: [x] if not isinstance(x, list) else x)
    df_exploded = df.explode('tags')
    
    tag_stats = df_exploded.groupby('tags').agg(
        session_count=('duration_seconds', 'count'),
        avg_duration_seconds=('duration_seconds', 'mean')
    ).reset_index()
    
    tag_stats['avg_duration_minutes'] = tag_stats['avg_duration_seconds'] / 60
    
    print("Tag Usage Analysis (Last 30 Days)")
    print("-" * 40)
    for _, row in tag_stats.iterrows():
        print(f"{row['tags']}: {row['session_count']} sessions, {row['avg_duration_minutes']:.1f} min avg")
    
    # Print top 3 most frequent tags
    top_tags = tag_stats.nlargest(3, 'session_count')
    print("\
Top 3 Tags:")
    print(f"1. {top_tags.iloc[0]['tags']} ({top_tags.iloc[0]['session_count']} sessions)")
    print(f"2. {top_tags.iloc[1]['tags']} ({top_tags.iloc[1]['session_count']} sessions)")
    print(f"3. {top_tags.iloc[2]['tags']} ({top_tags.iloc[2]['session_count']} sessions)")
else:
    print("No data available for analysis")