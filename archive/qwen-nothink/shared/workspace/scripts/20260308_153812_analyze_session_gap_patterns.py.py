"""Investigation: This script analyzes the gaps between sessions (untracked time) to reveal patterns in the Sovereign's operational rhythm. Unlike previous investigations that focused on session duration, this examines the time between sessions to understand workflow sequencing. The analysis groups gaps by the previous session's project type, revealing if training sessions (BBOY) lead to different gap patterns than coding sessions (STAR/SEIFUKU). This is the first investigation to directly examine session sequencing patterns, moving beyond duration to understand the Sovereign's natural workflow rhythm. The results will inform whether the Sovereign's rhythm aligns with strategic priorities (e.g., if training is followed by focused work, indicating effective sequencing).
Generated: 20260308_153812 UTC
"""

from supabase_helper import query_entries, entries_to_dataframe
import pandas as pd
from datetime import timedelta

# Get all entries for the last 30 days
entries = query_entries(days=30)

# Convert to DataFrame with proper time handling
df = entries_to_dataframe(entries)

# Sort by start time to ensure chronological order
df = df.sort_values('start').reset_index(drop=True)

# Calculate gaps between sessions (time between end of current session and start of next)
# This creates a new column for gaps, with NaN for the last session
df['gap_seconds'] = df['start'].shift(-1) - df['stop']
df['gap_seconds'] = df['gap_seconds'].dt.total_seconds()

# Create a column for the previous session's project type
# Using 'project_name' as the identifier for session types (STAR, SEIFUKU, BBOY, BOJ)
df['previous_project'] = df['project_name'].shift(1)

# Filter out sessions with missing previous project (first session)
df = df.dropna(subset=['previous_project'])

# Calculate average gap time for each previous session type
gap_analysis = df.groupby('previous_project')['gap_seconds'].mean().reset_index()
gap_analysis['average_gap'] = gap_analysis['gap_seconds'] / 3600  # Convert to hours

# Format output for readability
print("Session Gap Analysis by Previous Session Type:")
print("\
Average gap (hours) between sessions following each project type:")
print("\
" + "-" * 50)
for _, row in gap_analysis.iterrows():
    print(f"{row['previous_project']}: {row['average_gap']:.2f} hours")

# Compare with strategic targets
strategic_targets = {
    'STAR': 0.55,  # Target allocation
    'SEIFUKU': 0.15,
    'BBOY': 0.20,
    'BOJ': 0.10
}

# Check if gaps correlate with targets
print("\
\
Strategic Target Allocation vs. Gap Patterns:")
print("\
" + "-" * 50)
for project, target in strategic_targets.items():
    gap = gap_analysis[gap_analysis['previous_project'] == project]['average_gap'].values
    if len(gap) > 0:
        gap = gap[0]
        print(f"{project} target: {target:.0%} | Avg. gap: {gap:.2f}h")
    else:
        print(f"{project} target: {target:.0%} | No data for this project")