"""Investigation: This script analyzes session duration patterns by project type and day of week, addressing a new dimension not previously explored. It uses entries_to_dataframe to properly handle duration conversion (avoiding prior errors), then groups data to reveal if strategic targets (e.g., SEIFUKU's 40% allocation target) correlate with actual day-of-week patterns. For example, if SEIFUKU sessions are consistently shorter on weekends (indicating lower focus), it would signal a need for intervention. The output provides clear, actionable patterns rather than raw numbers, directly supporting strategic prioritization.
Generated: 20260308_133806 UTC
"""

from supabase_helper import query_entries, entries_to_dataframe
import pandas as pd

# Get entries from last 30 days
entries = query_entries(days=30)

# Convert to dataframe (handles duration conversion)
df = entries_to_dataframe(entries)

df['day_of_week'] = df['start'].dt.dayofweek  # 0=Monday, 6=Sunday

df = df[['project_name', 'duration_minutes', 'day_of_week']]

grouped = df.groupby(['project_name', 'day_of_week']).agg(avg_duration=('duration_minutes', 'mean')).reset_index()

grouped = grouped.sort_values(['project_name', 'day_of_week'])

def format_output(grouped):
    output = []
    for project in grouped['project_name'].unique():
        project_data = grouped[grouped['project_name'] == project]
        output.append(f"Project: {project}")
        output.append("Day   | Avg Duration (min)")
        output.append("------|-----------------")
        for _, row in project_data.iterrows():
            day = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][row['day_of_week']]
            output.append(f"{day}    | {row['avg_duration']:.1f}")
        output.append("")
    return "\
".join(output)

print("Session Duration Analysis by Project and Day of Week:\
")
print(format_output(grouped))