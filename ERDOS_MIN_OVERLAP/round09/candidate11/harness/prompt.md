You are an expert in optimization for the Erdős minimum overlap problem.

Problem: Find step function h: [0,2]->[0,1] with integral(h)=1 that minimizes
max_k integral h(x)(1-h(x+k)) dx. Target: beat C5 <= 0.38092303510845016.

CRITICAL INSIGHT: The seed optimizer already has good initialization patterns.
The bottleneck is NOT initialization—it's the OPTIMIZATION STRATEGY.

The seed runs 59,000 steps with fixed hyperparameters. This is too rigid.

YOUR STRATEGY:

1. Try DIFFERENT hyperparameter combinations systematically:
   - num_restarts: 5, 10, or more (seed only has 3)
   - base_learning_rate: try 0.002, 0.01, 0.05 (seed has 0.0053)
   - penalty_strength: try 1000, 3000, 8000 (seed has 1370)
   - num_steps: try 30000, 50000, 80000 (seed has 59000)

2. For EACH hyperparameter combination:
   a. Call edit_solution to update Hyperparameters in the EVOLVE-BLOCK
   b. Use probe_solution to get quick c5_bound (doesn't consume eval budget)
   c. If probe suggests improvement, run full evaluate_solution
   d. STOP and save if improved

3. Always check integral(h) ≈ 1 after edits. Adjust penalty if constraint is violated.

4. Use early stopping: if no improvement after 3 trials, try completely different strategy.

5. Target: combined_score > 1.0 (c5_bound < 0.380923)

What to edit in EVOLVE-BLOCK:
- Modify the Hyperparameters dataclass values
- Optionally add hyperparameter sweep logic to try multiple configs
- Ensure _objective_fn correctly computes constraint penalty
