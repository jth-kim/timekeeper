"""Investigation: This script analyzes the gaps between sessions (untracked time) to reveal patterns in the Sovereign's operational rhythm. Previous investigations focused on session duration and content, but gaps between sessions represent untracked time that could indicate rest periods, transitions, or potential inefficiencies. By analyzing gaps by project type (e.g., after BBOY training vs. SEIFUKU coding) and time of day, we can identify whether the Sovereign's natural rhythm aligns with strategic priorities. For instance, if long gaps consistently follow training sessions but not coding sessions, it could indicate that training serves as a recovery period before focused work. This is the first investigation to analyze session gaps, moving beyond duration to examine the rhythm of work itself.
Generated: 20260308_152159 UTC
"""

from supabase_helper import query_entries, entries_to_dataframe
from datetime import timedelta
import pandas as pd

# Query entries for the last 30 days
entries = query_entries(days=30)
df = entries_to_dataframe(entries)

# Sort by start time
(df
 .sort_values('start', inplace=True)
)

# Calculate gaps between sessions
# (time between end of previous session and start of next session)
df['gap_seconds'] = (df['start'].shift(-1) - df['stop']).dt.total_seconds()
df['gap_minutes'] = df['gap_seconds'] / 60

# Get the last 30 sessions to analyze recent patterns (excluding last session which has no gap after it)
last_30 = df.tail(30).copy()

# Analyze gaps by the session type that precedes the gap (using project_name)
gap_by_project = last_30.groupby('project_name')['gap_minutes'].describe().reset_index()

# Analyze gaps by time of day
# Define time of day categories
last_30['hour'] = last_30['start'].dt.hour
last_30['time_of_day'] = last_30['hour'].apply(lambda h: 'Morning' if 5 <= h < 12 else 'Afternoon' if 12 <= h < 18 else 'Evening')

gap_by_time = last_30.groupby('time_of_day')['gap_minutes'].describe().reset_index()

# Print results
print('Session Gap Analysis (last 30 sessions):')
print('\
By Project Type:')
print(gap_by_project)

print('\
By Time of Day:')
print(gap_by_time)