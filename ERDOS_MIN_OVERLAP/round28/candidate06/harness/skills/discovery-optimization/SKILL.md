---
name: discovery-optimization
description: "Pattern-based search for Erdos C5 minimization. Generate novel initializations (Gaussian peaks, sparse spikes, triangular), train quickly (30000 steps), screen with probe, validate with evaluate. Don't just tune hyperparameters - explore NEW solution structures."
---

# Novel Pattern Search for Erdos C5 Problem

## Why We Need New Patterns

The seed optimizer tries 15 patterns but all converge to similar local optima. To find c5_bound < 0.380923, we MUST explore fundamentally different initialization structures.

## Pattern Generation

1. CALL generate_patterns() to get novel initializations:
   - Gaussian peaks at various positions
   - Sparse spike patterns (few high-value regions)
   - Triangular distributions
   - Asymmetric distributions
   - Multi-modal patterns (4+ peaks)

2. Each returned pattern has precomputed c5_bound (analytical)
3. Keep patterns with c5_bound < 0.38 (already promising)

## Fast Training & Screening

1. EDIT pattern: set num_restarts=1 (one initialization), num_steps=30000 (fast)
2. CALL probe_solution (cheap, ~10s) to check if training improves the pattern
3. If probe shows c5_bound < 0.375, CALL evaluate_solution for final validation

## Pattern Exploration Strategy

- Start with 3-5 different pattern types from generate_patterns
- For each, run fast training + probe + (maybe) full eval
- This lets you screen 10+ different pattern structures in 20 evals
- Then DOUBLE DOWN on the best pattern type, try variations

## Common Pitfalls

- DON'T just tune hyperparameters on the same pattern
- DON't skip probe - waste evals on bad patterns
- DON't use num_steps=59000 for all patterns - too slow for screening
- DO try at least 3-5 different pattern types before giving up

## Expected Workflow

1. generate_patterns -> get 3 patterns
2. Train each with 30000 steps -> probe all 3
3. Pick best -> evaluate -> if <0.375, REPORT SUCCESS
4. If no success, try different pattern templates
5. If STILL stuck, try hyperparameter tuning on the best pattern
