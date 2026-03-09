"""Investigation: This investigation moves beyond project types (SEIFUKU/STAR/BBOY) to analyze session length through the lens of activity tags - a new dimension in the data. The tag [👾 Coding] consistently appears in work sessions while [⚡️ Training] appears in physical sessions. This reveals whether coding sessions (which require deeper focus) have different duration patterns than training sessions. The result will inform energy management strategies and validate if the current project type categorization aligns with actual work characteristics. This is the first time we're using description tags as a primary analytical lens rather than project types.
Generated: 20260308_112558 UTC
"""

from supabase_helper import query_entries, entries_to_dataframe
import pandas as pd

# Query last 30 days of entries
entries = query_entries(days=30)
df = entries_to_dataframe(entries)

df['activity_type'] = df['description'].apply(lambda desc: 'Coding' if '[👾 Coding]' in desc else 'Training' if '[⚡️ Training]' in desc else 'Other')

# Calculate average duration in minutes
avg_coding = df[df['activity_type'] == 'Coding']['duration_minutes'].mean()
avg_training = df[df['activity_type'] == 'Training']['duration_minutes'].mean()

# Print results
print(f"{'Activity Type':<15} {'Avg. Length (min)':>15}")
print(f"{'-'*15} {'-'*15}")
print(f"{'Coding':<15} {avg_coding:15.2f}")
print(f"{'Training':<15} {avg_training:15.2f}")