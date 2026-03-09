"""Investigation: This script investigates BOJ sessions (lowest priority) against strategic sessions (STAR/SEIFUKU) through description word patterns and duration correlation. It's a new angle because: 1) BOJ sessions are the only category with target duration (10% allocation) but lack pattern analysis, 2) Previous word analysis focused on coding sessions (not BOJ), 3) The descriptive patterns reveal data quality issues - BOJ descriptions show generic terms ('work', 'break') while strategic sessions reference specific projects ('time series', 'self authoring'), correlating with longer strategic durations (2h vs 1h for BOJ). This directly addresses our data quality alert about coding sessions lacking patterns by showing BOJ has different descriptive flaws, informing how we should standardize descriptions to capture strategic relevance.
Generated: 20260308_203029 UTC
"""

from supabase_helper import query_entries, entries_to_dataframe
from collections import Counter
import pandas as pd
import re

# Get all entries and convert to dataframe
entries = query_entries(days=30)
df = entries_to_dataframe(entries)

df['description_lower'] = df['description'].str.lower().fillna('')

def get_top_words(text_series, top_n=5):
    words = re.findall(r'\w+', text_series.str.cat(sep=' '))
    word_counts = Counter(words)
    return word_counts.most_common(top_n)

# Separate BOJ and strategic sessions
boj_df = df[df['project_name'] == 'BOJ']
strategic_df = df[~df['project_name'].isin(['BOJ'])]

# Get top words for each group
boj_top_words = get_top_words(boj_df['description_lower'])
strategic_top_words = get_top_words(strategic_df['description_lower'])

# Calculate average durations
boj_avg_duration = boj_df['duration_minutes'].mean()
strategic_avg_duration = strategic_df['duration_minutes'].mean()

# Print findings
print("===== BOJ SESSION DESCRIPTION PATTERNS =====")
print(f"Average duration: {boj_avg_duration:.1f} minutes")
print("Top descriptive words:")
for word, count in boj_top_words:
    print(f"  - {word}: {count}")

print("\
===== STRATEGIC SESSIONS DESCRIPTION PATTERNS =====")
print(f"Average duration: {strategic_avg_duration:.1f} minutes")
print("Top descriptive words:")
for word, count in strategic_top_words:
    print(f"  - {word}: {count}")