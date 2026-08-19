---
name: pattern-mutation-strategy
description: Directly edit pattern parameters (marks, peaks, thresholds) in the seed code. Focus on Golomb ruler and tri-modal patterns.
---

# Pattern Mutation Strategy for Erdos C5

## Why Pattern Parameters Matter

The seed program has HARDCODED pattern parameters. Small changes can significantly improve c5_bound.

## Pattern 12: Golomb Ruler (MOST PROMISING)

Current: marks = [0.0, 0.4, 0.8, 1.2, 1.6]

Try editing to:
- [0.0, 0.35, 0.7, 1.05, 1.4]  # smaller spacing
- [0.0, 0.3, 0.6, 0.9, 1.2]  # even tighter
- [0.0, 0.25, 0.5, 0.75, 1.0]  # quarter spacing
- [0.0, 0.333, 0.667, 1.0, 1.333]  # thirds

Key insight: Golomb rulers minimize overlaps when marks are WELL SPACED.

## Pattern 14: Tri-Modal

Current: peaks = [0.4, 1.0, 1.6]

Try editing to:
- [0.3, 0.9, 1.5]  # spread wider
- [0.25, 1.0, 1.75]
- [0.35, 1.05, 1.65]  # slightly offset from center
- [0.2, 1.0, 1.8]

Key insight: Peaks should NOT be too close to [0.5] where overlap is worst.

## Pattern 5: Bipartite (Baseline)

Current: a = 0.5

Try: a = 0.4, 0.45, 0.55, 0.6

## Workflow

1. CALL pattern_analyzer to see current baseline performance
2. EDIT the EVOLVE-BLOCK to change ONE pattern parameter at a time
3. CALL probe_solution to check if improvement
4. If c5_bound < 0.375 (combined_score > 1.002), CALL evaluate_solution
5. Repeat with different patterns

## What NOT to do

- Don't change num_intervals, learning_rate, penalty_strength (training hyperparameters)
- These affect how the optimizer TRAINS, but we need to change the PATTERNS themselves
- Focus on marks, peaks, thresholds - the actual construction parameters
