---
name: discovery-optimization
description: "Optimize an Erdos minimum overlap problem solver by exploring the design space of hyperparameters\nand program structure. Use `analyze_structure` to get data-driven recommendations, then try\ncoarse-to-fine exploration of num_intervals. Make one substantive change per iteration.\nRemember: validity=0 means a crash or constraint violation; combined_score > 1.0 means a new record."
---

# Erdos optimization with design-space exploration

## Phase 1: Baseline analysis

**CRITICAL**: Call `analyze_structure` ONCE at the very beginning to understand your current config.
It reports: num_intervals, penalty_strength, and recommendations for improvement.

## Phase 2: Coarse-to-fine exploration

The seed uses num_intervals=200. This may be too coarse for optimal structure.

Strategy:
1. **Coarse**: Start with num_intervals=50-100 to find a good ballpark solution
2. **Refine**: If coarse works, use SEARCH/REPLACE to increase to num_intervals=200, then 500
3. **Alternative**: If 200 fails, try num_intervals=300-400 directly

Use targeted SEARCH/REPLACE on this line:
`num_intervals: int = 200`

## Phase 3: Hyperparameter tuning

If the constraint isn't satisfied (integral != 1), adjust penalty_strength:
- If constraint_loss is high, INCREASE penalty_strength
- If integral consistently overshoots, INCREASE penalty_strength
- If integral consistently undershoots, DECREASE penalty_strength

Test penalty_strength values: 10000, 50000, 100000, 500000, 1000000, 2000000

## Phase 4: Diverse restarts

If you're stuck, try a NEW program with:
- Different initial random seed (change jax.random.PRNGKey(42) to 123, 456, etc.)
- Different optimizer (Adam, RMSprop, AdaGrad)
- Different num_steps (10000, 50000, 100000)

## Phase 5: Validation

- combined_score > 1.0 means you've beaten the seed!
- validity=0 means the program crashed or violated constraints - read the error
- If valid but score lower than best_so_far, try a DIFFERENT approach, not just tuning

## Tool call discipline

- `analyze_structure`: Call ONCE at start, then don't need it again
- `evaluate_solution`: Your real budget - use for promising configs only
- `probe_solution`: Don't rely on it for this task - it's for slow evaluators with subsampled data
- `edit_solution`: Make one substantive change per call
- `finish`: When you cannot improve or budget is low
