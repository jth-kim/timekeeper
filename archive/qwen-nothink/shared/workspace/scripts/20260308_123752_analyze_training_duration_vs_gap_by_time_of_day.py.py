"""Investigation: This script investigates whether training session length directly correlates with subsequent recovery time (gap), and whether this relationship varies by time of day. Previous investigations focused on training timing (e.g., after 4PM) or training-coding sequences, but not the direct relationship between training duration and gap. The analysis reveals if longer training sessions require proportionally longer recovery, which would validate energy management strategies. The time-of-day breakdown addresses the unexplored question of whether morning training (when energy is higher) creates different recovery patterns than afternoon training. This is the first investigation to quantify the causal relationship between training duration and gap duration, moving beyond qualitative observations.
Generated: 20260308_123752 UTC
"""

from supabase_helper import query_entries, entries_to_dataframe
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Query all entries for last 30 days
entries = query_entries(days=30)
if not entries:
    print("No entries found")
    exit()

# Convert to DataFrame with proper duration handling
df = entries_to_dataframe(entries)

df['end'] = df['start'] + pd.to_timedelta(df['duration_seconds'], unit='s')

# Sort by start time
df = df.sort_values('start').reset_index(drop=True)

# Create next session start column
df['next_start'] = df['start'].shift(-1)

# Filter for training sessions (with ⚡️ Training tag)
training_mask = df['tags'].apply(lambda tags: '⚡️ Training' in tags)
training_df = df[training_mask].copy()

# Calculate gap duration (next session start - current session end)
training_df['gap_seconds'] = (training_df['next_start'] - training_df['end']).dt.total_seconds()
training_df['training_duration_minutes'] = training_df['duration_seconds'] / 60
training_df['gap_minutes'] = training_df['gap_seconds'] / 60

# Remove rows without next session (last entry)
training_df = training_df.dropna(subset=['next_start'])

# Add time of day category
training_df['time_of_day'] = training_df['start'].apply(
    lambda x: 'morning' if x.hour < 12 else 'afternoon'
)

# Compute correlation by time of day
morning_corr = training_df[training_df['time_of_day'] == 'morning'].corr('pearson')['training_duration_minutes']['gap_minutes']
afternoon_corr = training_df[training_df['time_of_day'] == 'afternoon'].corr('pearson')['training_duration_minutes']['gap_minutes']

# Print findings
print("\
Training Session Analysis (n={})".format(len(training_df)))
print("- Average training duration: {:.1f} min".format(training_df['training_duration_minutes'].mean()))
print("- Average gap duration: {:.1f} min".format(training_df['gap_minutes'].mean()))
print("\
Correlation by time of day:")
print("  Morning sessions: {:.2f}".format(morning_corr))
print("  Afternoon sessions: {:.2f}".format(afternoon_corr))

# Generate scatter plot
plt.figure(figsize=(10, 6))
for time_of_day, group in training_df.groupby('time_of_day'):
    plt.scatter(group['training_duration_minutes'], group['gap_minutes'], 
                label=time_of_day.title(), alpha=0.7)
    
    # Add regression line
    z = np.polyfit(group['training_duration_minutes'], group['gap_minutes'], 1)
    p = np.poly1d(z)
    plt.plot(group['training_duration_minutes'], p(group['training_duration_minutes']), 
             "--", label="{} trend".format(time_of_day))

plt.xlabel('Training Duration (minutes)')
plt.ylabel('Gap to Next Session (minutes)')
plt.title('Training Duration vs. Subsequent Gap by Time of Day')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('/data/workspace/results/training_gap_correlation.png')

# Print key insight
if morning_corr > 0.5 or afternoon_corr > 0.5:
    print("\
INSIGHT: Strong positive correlation detected - longer training sessions correlate with longer recovery gaps, especially in the {}.")
else:
    print("\
INSIGHT: No significant correlation found - training duration does not consistently predict gap duration.")