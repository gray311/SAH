---
name: discovery-optimization
description: "Hyperparameter sweep optimization for Erdos minimum overlap.\nSystematically explore (lr, penalty, num_restarts, num_steps) combinations\nwith probe ranking before full evaluation."
---

# Erdos C5 Optimization - Hyperparameter Sweep Strategy

## Why This Works
The seed optimizer has decent initialization but rigid hyperparameters.
Systematic exploration of the hyperparameter space finds configurations
that escape local minima.

## Strategy
1. Define hyperparameter grid to explore:
   - num_restarts: [3, 5, 8, 12] (more restarts help escape local minima)
   - base_learning_rate: [0.002, 0.005, 0.01, 0.02] (adaptive LR helps)
   - penalty_strength: [500, 1000, 2000, 5000] (balance constraint vs. objective)
   - num_steps: [30000, 50000, 80000] (more steps allow finer optimization)

2. For each combination:
   - Edit EVOLVE-BLOCK to update Hyperparameters
   - Check integral(h) ≈ 1 (constraint must be satisfied)
   - Call probe_solution to get quick c5_bound estimate
   - If probe score < current best, call evaluate_solution
   - Track best combined_score found

3. Probing workflow:
   - Start with seed hyperparameters, probe first
   - Modify one hyperparameter at a time
   - Probe each variant (fast, ~10s)
   - Only full-evaluate promising variants

4. Key edits needed:
   - Add new Hyperparameters instances in EVOLVE-BLOCK
   - May need to add a loop to try multiple restart configs internally
   - Ensure _objective_fn penalty term is correctly scaled

5. Success criteria:
   - Find c5_bound < 0.38092303510845016
   - Report combined_score > 1.0

## Pro Tips
- Higher num_restarts with moderate LR works well
- Penalty should be large enough to enforce integral=1 but not dominate objective
- Watch for gradient explosion: if loss jumps, reduce LR
- Use probe budget wisely: ~15 probes, then 10-15 full evals
