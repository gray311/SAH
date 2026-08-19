---
name: discovery-optimization
description: "Iteratively optimize programs through diverse search strategies (random restarts, adaptive hyperparameter tuning, simulated annealing) to escape local minima and discover better solutions."
---

# Adaptive Search Optimization for Non-Convex Problems

This harness uses an **orchestrated search** approach rather than simple parameter tuning. Each edit should implement one of these strategies:

## Strategy 1: Hyperparameter Grid Search
Systematically explore combinations of:
- num_intervals: 50, 100, 200, 400, 800 (more intervals = finer resolution but slower)
- learning_rate: 0.001, 0.005, 0.01, 0.05 (adaptive for different scale)
- num_steps: 5000, 10000, 20000, 50000 (balance between convergence and runtime)
- penalty_strength: 10000, 100000, 1000000, 10000000 (tune constraint enforcement)

## Strategy 2: Random Restarts
When stuck in local minima:
- Reset latent_h_values with new RNG seeds (try 3-5 seeds per run)
- Keep best intermediate h values across restarts
- Use warm restarts: take best h from failed run, perturb, continue training

## Strategy 3: Adaptive Resolution
- Start coarse (50-100 intervals) for fast exploration
- If promising results, increase resolution (400-800 intervals)
- Can use multi-resolution approach: coarse for direction, fine for polish

## Strategy 4: Penalty Adaptation
- Monitor constraint violation: integral_h - 1.0
- If constraint poorly satisfied, increase penalty_strength
- If objective barely improving with perfect constraints, reduce penalty
- Can use adaptive schedule: start high, decay over training

## Strategy 5: Optimizer Variants
- Try SGD with momentum vs Adam
- Try learning rate schedules: decay over steps, warmup then decay
- Consider adaptive batch learning (though this is implicit optimization)

## Implementation Pattern
For each evaluation, implement ONE strategy with COMPLETE implementation:

1. Define the strategy (e.g., "10 random restarts with varied seeds")
2. Write full code implementing it (no stubs, no comments about TODO)
3. Ensure runtime is reasonable (< evaluation timeout)
4. Return best result across all variations

## Recovery
- If validity=0: Fix the crash (often NaN/infinity from bad optimization)
- If score < best_so_far: Your strategy is worse; try a genuinely different one
- If progress stalls (< 0.001 improvement in 3 runs): Switch strategy entirely
- With 20 evaluations, each must contribute meaningfully

## Final Tip
The goal is beating C5 <= 0.3809. Track the c5_bound metric directly. A combined_score > 1.0 means c5_bound < 0.3809 (a new record!).
