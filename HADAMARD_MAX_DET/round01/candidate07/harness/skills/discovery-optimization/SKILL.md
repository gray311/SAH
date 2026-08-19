---
name: discovery-optimization
description: "Iteratively optimize a program EVOLVE-BLOCK to maximize automatic evaluator score under fixed evaluation budget. Use for construction algorithm-speed and heuristic discovery tasks scored by combined_score (higher is better) through edit_solution evaluate_solution finish tools. IMPORTANT TRY MULTIPLE approaches and seeds per evaluation for combinatorial tasks to increase success probability"
---

# Discovery optimization - COMBINATORIAL STRATEGY

One tool call per turn: `edit_solution` to stage a full new EVOLVE-BLOCK, then `evaluate_solution` to score it. `combined_score` is higher-is-better; the best version is retained automatically.

## CRITICAL STRATEGY: DIVERSITY OF APPROACHES

For tasks like Hadamard matrix construction where the search space is enormous, NEVER rely on a single construction method or random seed. Instead, write code that internally:

1. Tries multiple random seeds: `for seed in [42, 123, 456, 789, 10111]: try construction(seed); keep best`

2. Tries multiple construction methods:
   - Quadratic residue initialization
   - Random initialization
   - Greedy construction (fill diagonal 1, then try to satisfy orthogonality constraints)
   - Structured patterns (circulant block-based, etc.)

3. Tries multiple optimization strategies:
   - Simulated annealing with different temperature schedules
   - Pure hill climbing (no annealing)
   - Genetic algorithms (maintain population crossover/mutate)
   - Local search from different starting points

4. Tries multiple iteration counts: 500, 2000, 5000 iterations - use the time limit safely (aim for 200s per eval).

After exploration, return the SINGLE BEST result.

## Execution Flow

1. Read the task score objective (maximize determinant absolute value).
2. Identify constraints (matrix must be +/-1, exactly n x n where n=29, time limit 350s).
3. Write code that loops over multiple seeds and/or methods.
4. For each variant, run the construction and optimization.
5. Track the best (|det|, matrix) across all variants.
6. Return only the best result.

## Avoid These Pitfalls

- Do not use a fixed seed without variation - this limits exploration.
- Do not overwrite the best result - maintain best_det and best_matrix throughout.
- Do not run an optimization that takes >300s - test locally or estimate iterations.
- Do not try one approach - always diversify.

## Recovery

If validity=0, the program crashed or violated constraints. Fix the specific error. If score is lower, the diversity did not help - add MORE methods (genetic algorithm, different initialization patterns) or MORE seeds.

## When to Finish

Use all 20 evaluations wisely. When you cannot improve diversity or scores plateau, call `finish` with a summary of your best approach.
