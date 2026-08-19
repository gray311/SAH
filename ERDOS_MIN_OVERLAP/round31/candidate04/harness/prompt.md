Erdos C5 problem: Find step function h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

CONSTRAINTS: integral(h)=1, h in [0,1].

CURRENT BEST: c5_bound = 0.38092303510845016 (combined_score=1.0)
GOAL: Find c5_bound < 0.38092303510845016 (combined_score > 1.0)

SEARCH STRATEGY:
1. Edit the EVOLVE-BLOCK to replace the multi-restart optimization with simpler gradient descent
2. Key hyperparameter changes:
   - num_intervals: 800 -> 200 (faster evaluation)
   - base_learning_rate: 0.004 -> 0.001 (more stable)
   - num_steps: 120000 -> 50000 (focus on quality)
   - penalty_strength: 61.0 -> 30.0 (less constraint)
   - num_restarts: 3 -> 5 (more trials per eval)
3. Use gradient descent on sigmoid-transformed latent vector
4. Each restart uses different random seed and hyperparameters
5. Return best c5_bound across all restarts

TOOL USAGE:
- edit_solution: Apply the hyperparameter changes above
- evaluate_solution: Check if combined_score > 1.0
- probe_solution: Optional fast screening (c5_bound < 0.375)
