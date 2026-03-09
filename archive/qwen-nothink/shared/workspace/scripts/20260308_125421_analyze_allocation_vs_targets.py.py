"""Investigation: This script analyzes whether actual time allocation across project types aligns with strategic targets defined in the alert thresholds config. It calculates the percentage of time spent on each project type (STAR, BBOY, SEIFUKU, BOJ), compares it to the target percentages, and identifies if deviations exceed the defined drift threshold (25%). This is the first investigation to directly connect data patterns to the strategic targets that inform our alert system. Previous analyses focused on session sequences or durations, but this evaluates whether the allocation strategy itself is working. The results will directly inform whether we need to adjust the Sovereign's approach or refine the targets themselves. This investigation is critical because it moves beyond descriptive analysis to strategic evaluation - a core COO function.
Generated: 20260308_125421 UTC
"""

from supabase_helper import query_entries, entries_to_dataframe
from supabase_helper import parse_duration_seconds
import pandas as pd

# Get all entries from last 30 days
entries = query_entries(days=30)
df = entries_to_dataframe(entries)

# Define target allocations from config
config_targets = {
    'STAR': 0.55,
    'BBOY': 0.20,
    'SEIFUKU': 0.15,
    'BOJ': 0.10
}

def get_project_type(entry):
    # Extract project name from project_name field
    # Example: 'STAR', 'BBOY', 'SEIFUKU', 'BOJ'
    project_name = entry['project_name']
    if 'STAR' in project_name:
        return 'STAR'
    elif 'BBOY' in project_name:
        return 'BBOY'
    elif 'SEIFUKU' in project_name:
        return 'SEIFUKU'
    elif 'BOJ' in project_name:
        return 'BOJ'
    return 'OTHER'

# Apply project type classification
df['project_type'] = df.apply(get_project_type, axis=1)

df = df[df['project_type'].isin(config_targets.keys())]

# Calculate actual allocation
actual_allocations = df.groupby('project_type')['duration_minutes'].sum().reset_index()
actual_allocations['percentage'] = actual_allocations['duration_minutes'] / actual_allocations['duration_minutes'].sum() * 100

# Compare to targets
results = []
for project_type, row in actual_allocations.iterrows():
    target = config_targets[row['project_type']]
    actual = row['percentage']
    deviation = actual - target * 100
    results.append({
        'project_type': row['project_type'],
        'actual_percentage': round(actual, 1),
        'target_percentage': target * 100,
        'deviation': round(deviation, 1),
        'exceeds_threshold': abs(deviation) > 25  # Drift threshold from config
    })

# Format and print results
print('=== ACTUAL TIME ALLOCATION VS TARGETS ===')
print('Project Type | Actual (%) | Target (%) | Deviation (%) | Within Threshold?')
print('-' * 70)
for res in results:
    threshold_met = 'Yes' if not res['exceeds_threshold'] else 'NO'
    print(f"{res['project_type']:<12} | {res['actual_percentage']:>10.1f} | {res['target_percentage']:>10.1f} | {res['deviation']:>13.1f} | {threshold_met}")

# Additional analysis: Check for persistence
if len(df) > 0:
    total_duration = df['duration_minutes'].sum()
    print(f"\
Total tracked time: {total_duration:.1f} minutes ({total_duration/60:.1f} hours)")
    print(f"\
Note: Drift threshold is {config_targets['drift_threshold']*100}% based on config")