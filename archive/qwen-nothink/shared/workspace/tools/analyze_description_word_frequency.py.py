"""Investigation: This script analyzes the free-text session descriptions to uncover word patterns that may correlate with coding sessions. It's a new angle that hasn't been explored in previous investigations (which focused on tags, project types, or durations). By examining what words appear most frequently in descriptions, we can identify if certain phrases or topics correlate with coding sessions (which require deeper focus) and whether these patterns relate to session duration. This builds on our recent work on [👾 Coding] tags but moves beyond tags to analyze the actual language used in descriptions. The findings could help refine how the Sovereign structures sessions for optimal focus and productivity.
Generated: 20260308_134843 UTC
"""

from supabase_helper import query_entries, entries_to_dataframe
from collections import Counter
import re
import pandas as pd

# Get all entries and convert to dataframe with proper duration handling
entries = query_entries(days=30)
df = entries_to_dataframe(entries)

def clean_text(text):
    # Convert to lowercase and remove punctuation
    if not isinstance(text, str):
        return ""
    return re.sub(r'[\W_]+', ' ', text.lower())

def get_top_words(descriptions, n=10):
    all_words = []
    for desc in descriptions:
        if isinstance(desc, str):
            words = clean_text(desc).split()
            all_words.extend(words)
    return Counter(all_words).most_common(n)

# Filter for coding sessions
coding_sessions = df[df['tags'].apply(lambda x: '[👾 Coding]' in x if isinstance(x, list) else False)]
non_coding_sessions = df[~df.index.isin(coding_sessions.index)]

# Get top words in coding vs non-coding descriptions
coding_words = get_top_words(coding_sessions['description'].tolist())
non_coding_words = get_top_words(non_coding_sessions['description'].tolist())

def format_words(words):
    return ', '.join([f"{word} ({count})" for word, count in words])

def format_comparison(coding_words, non_coding_words):
    print("\
Top words in coding session descriptions:")
    print(f"{format_words(coding_words)}\
")
    
    print("Top words in non-coding session descriptions:")
    print(f"{format_words(non_coding_words)}\
")

format_comparison(coding_words, non_coding_words)

# Check if top words correlate with session duration
if not coding_sessions.empty:
    coding_sessions['duration_minutes'] = coding_sessions['duration_minutes'].fillna(0)
    top_coding_words = [word for word, _ in coding_words]
    
    print("\
Correlation between top words and coding session duration:")
    for word in top_coding_words[:3]:  # Check top 3 words
        filtered = coding_sessions[coding_sessions['description'].str.contains(word, case=False, na=False)]
        if not filtered.empty:
            avg_duration = filtered['duration_minutes'].mean()
            print(f"- '{word}' sessions: {avg_duration:.1f} minutes (n={len(filtered)})")
        else:
            print(f"- '{word}' not found in coding descriptions")