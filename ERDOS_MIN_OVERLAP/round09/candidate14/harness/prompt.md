You are an expert in numerical optimization for the Erdős minimum overlap problem.

Goal: Beat C5 <= 0.38092303510845016 by finding h: [0,2]->[0,1] with integral(h)=1
that minimizes max_k integral h(x)(1-h(x+k))dx.

KEY INSIGHT: The seed program already has excellent multi-pattern initialization (12 variants).
Your job is NOT to create new initializations, but to SYSTEMATICALLY TUNE the optimizer
parameters to escape local minima and find a better c5_bound.

STRATEGY: ITERATIVE HYPERPARAMETER OPTIMIZATION

1. Call hyperparameter_sweep() to get ~5 diverse optimizer configurations
   (learning rates, penalty strengths, restart counts, step schedules)

2. For each config:
   - Run a short test with probe_solution (1000 steps each, very cheap)
   - Keep configs that show promise

3. For top 2-3 configs from probing, run full optimization with evaluate_solution

4. If best score improves, edit the EVOLVE-BLOCK to use the winning config
5. Repeat with slight variations around the winning config

What to edit in EVOLVE-BLOCK:
- Hyperparameters: num_intervals, base_learning_rate, num_steps, penalty_strength, num_restarts
- Try: num_intervals=600-1200, lr=0.001-0.02, penalty=1000-10000, num_steps=30000-70000, num_restarts=1-5

Target: combined_score > 1.0 (c5_bound < 0.38092303510845016)
