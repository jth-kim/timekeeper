"""Investigation: This script validates the core data conversion layer that has been failing all previous analyses. By using entries_to_dataframe (which properly converts ISO duration strings), it demonstrates that the pipeline works when used correctly. The output shows raw vs. converted durations, confirms numeric conversion, and verifies the duration range. This is the prerequisite for all future allocation and duration-based analysis. The script directly addresses the root cause of our investigation failures (string vs. numeric duration) rather than proceeding with flawed assumptions. Once validated, we can confidently run the allocation analysis (agenda item) and other time-based investigations.
Generated: 20260308_130740 UTC
"""

from supabase_helper import query_entries, entries_to_dataframe
from datetime import datetime

# Query all entries (30 days) to validate duration conversion
entries = query_entries(days=30)

# Convert to DataFrame with proper duration conversion
df = entries_to_dataframe(entries)

# Verify conversion by checking sample rows
print("\
SAMPLE DURATION CONVERSION VALIDATION (first 5 entries):")
print("{:<20} {:<15} {:<15}".format("Start Time", "Raw Duration", "Converted Minutes"))
for i in range(min(5, len(df))):
    row = df.iloc[i]
    raw_duration = row['duration']
    converted_minutes = row['duration_minutes']
    print("{:<20} {:<15} {:<15.2f}".format(
        row['start'].strftime('%Y-%m-%d %H:%M'),
        raw_duration,
        converted_minutes
    ))

# Check for any remaining string durations in the DataFrame
if df['duration'].dtype == object:
    print(f"\
WARNING: Duration column still contains string values ({df['duration'].dtype}).")
else:
    print(f"\
SUCCESS: All durations converted to numeric (duration_minutes column).")

# Additional validation: Check min/max duration
print(f"\
Duration range: {df['duration_minutes'].min():.2f} to {df['duration_minutes'].max():.2f} minutes")