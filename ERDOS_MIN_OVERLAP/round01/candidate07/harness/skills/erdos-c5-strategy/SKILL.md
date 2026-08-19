---
name: erdos-c5-strategy
description: Expert strategy for optimizing the Erdős C5 bound using local search and probe-based ranking. Call this when the current approach is gradient descent or exhaustive search.
---

# Erdős C5 Optimization: Local Search Strategy

## Why Local Search Works Better Here
The C5 landscape is non-convex with many local minima. Gradient descent (20k steps) often gets stuck. Local search over a smaller parameter space is faster and can escape bad regions.

## Step-by-Step Approach

1. **Start Small**: Begin with 50-100 intervals. Less computation, faster iteration.

2. **Local Search Loop**:
   - Use `local_search_step` with `reduce_intervals` to find the minimal intervals needed.
   - Once stable, try `increase_intervals` to see if more precision helps.
   - Use `adjust_breakpoints` to fine-tune breakpoint positions.
   - Use `perturb_values` to adjust the h(x) values.

3. **Probe Before You Commit**:
   - After each `local_search_step`, use `probe_solution` to rank.
   - Only call `evaluate_solution` when probe_score shows >5% improvement over baseline.

4. **Iterative Refinement**:
   - Cycle through: reduce → probe → evaluate → increase → probe → evaluate
   - Keep what works, abandon what doesn't.

5. **Endgame**:
   - When no local search improvement in 3+ rounds, try a fresh random start with fewer intervals.

## Red Flags
- Full evaluation taking >30s: reduce intervals immediately.
- Probe score worse than baseline: revert and try different change_type.
- No improvement in 5 rounds: increase temperature, try fresh initialization.
