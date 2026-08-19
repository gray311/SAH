---
name: discovery-optimization
description: "Minimal-edit strategy for Erdos minimum overlap optimization with probe-based validation."
---

# Erdos Minimum Overlap - Minimal Edit Strategy

## Why Minimal Edits Work

The optimization landscape has MANY local optima. Complex edits that rewrite multiple components
often break things. Simple, targeted changes with immediate probe validation work better.

## Workflow:

1. **Analyze first**: Call analyze_correlation_spectrum() to understand:
   - What the current correlation looks like
   - Where the maximum overlap occurs
   - Whether the integral constraint is satisfied

2. **Make ONE small edit**: Examples:
   - Change learning_rate from 0.0053 to 0.01
   - Change penalty_strength from 1370 to 5000
   - Change num_intervals from 800 to 1600
   - Add ONE construction type to _get_best_initialization

3. **Probe immediately**: Call probe_solution() to check if this edit helps BEFORE using an evaluation

4. **Evaluate only if probe improves**: Don't waste the 30 evaluation budget

5. **Iterate**: If no improvement after 3 tries, try a different construction pattern

## Construction Patterns to Try:
- **bimodal_tight**: Two peaks at 0.25 and 0.75
- **triangular**: Linear ramps at 0.33 intervals
- **periodic**: Simple alternation on [0,0.5]
- **golomb_5**: Mark-based spacing

## Key Principles:
- ONE edit at a time
- Probe before every full evaluation
- Save best score; only keep edits that improve
- Remember: c5_bound should be < 0.380923 for success
