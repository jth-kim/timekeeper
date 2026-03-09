"""Investigation: This script analyzes the trend of training sessions over two consecutive 30-day periods. It compares the number of training sessions in the current 30 days (which was 16 sessions) with the previous 30 days to determine if the low training frequency represents a downward trend. This directly addresses the agenda item about whether the training frequency is due to lack of time or lack of prioritization. Unlike previous investigations that analyzed current session counts without historical context, this establishes a trend that will determine whether the low training frequency is a temporary dip or a systemic issue requiring intervention.
Generated: 20260308_114140 UTC
"""

from supabase_helper import query_entries, entries_to_dataframe
import pandas as pd
from datetime import datetime, timedelta

# Get current time
current_time = datetime.utcnow()

# Get last 60 days of entries
entries = query_entries(days=60)
df = entries_to_dataframe(entries)

# Filter for training sessions (tag: [⚡️ Training])
training_sessions = df[df['tags'].apply(lambda tags: '[⚡️ Training]' in tags)]

# Split into two 30-day periods
# Current 30 days: from 30 days ago to now
current_period_start = current_time - timedelta(days=30)
current_period_end = current_time
previous_period_start = current_time - timedelta(days=60)
previous_period_end = current_time - timedelta(days=30)

# Filter training sessions for each period
current_training = training_sessions[
    (training_sessions['start'] >= current_period_start) & 
    (training_sessions['start'] <= current_period_end)
]

previous_training = training_sessions[
    (training_sessions['start'] >= previous_period_start) & 
    (training_sessions['start'] <= previous_period_end)
]

# Count sessions in each period
current_count = len(current_training)
previous_count = len(previous_training)

# Calculate percentage change
if previous_count > 0:
    change_percent = ((current_count - previous_count) / previous_count) * 100
else:
    change_percent = None

# Print findings
print("Training Session Trend Analysis (Last 60 Days)")
print(f"Current 30 days (last 30 days): {current_count} sessions")
print(f"Previous 30 days (30-60 days ago): {previous_count} sessions")
if change_percent is not None:
    print(f"Change: {change_percent:.2f}%")
    if change_percent < 0:
        print("Trend: Decreasing")
    elif change_percent > 0:
        print("Trend: Increasing")
    else:
        print("Trend: Stable")
else:
    print("Cannot calculate trend (previous period had 0 sessions)")