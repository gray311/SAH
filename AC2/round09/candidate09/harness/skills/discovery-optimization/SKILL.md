---
name: discovery-optimization
description: "Optimize program parameters to maximize C\u2082 score. The seed already uses proven step-function search at 1.03431. Task is parameter tuning, not function discovery."
---

# Parameter Optimization for C₂ Maximization

Core Principle: The seed step-function search at 1.03431 is already superior to AlphaEvolve's record. 
Your job is FINE-TUNING existing hyperparameters, not discovering new function classes.

Available Parameters to Tune:
- learning_rate: Controls gradient step size (try 0.18-0.28 range)
- num_intervals: Function discretization (try 350-450 range)
- num_steps: Total optimization iterations (try 30000-45000)
- warmup_steps: Initial learning rate warmup (try 3000-5000)
- reinit_fraction: Fraction of function to reinitialize periodically
- reinit_std: Standard deviation for random reinitialization
- pattern_idx: Which step-function template to use (0-12 in seed)

Strategy:
1. Start by reading the seed program to understand current parameter values
2. Pick ONE parameter to adjust by 10-20% (don't change multiple at once)
3. Use edit_solution with targeted SEARCH/REPLACE - change ONLY that parameter line
4. evaluate_solution and observe: did score improve, drop, or error?
5. If score improved, try similar adjustments (+/- small amounts)
6. If score dropped or error, revert direction or try different parameter
7. Track your best score; best version is kept automatically
8. Near the end, consolidate: make final edits count toward beating 1.03431

Safety Rules:
- NEVER change class definitions, imports, or function signatures outside EVOLVE-BLOCK
- NEVER remove required methods or break Python syntax
- Keep internal search/optimization loops within time limits (seed uses ~37000 steps safely)
- When low on evaluations (<5), only make 1-2 parameter changes left

Remember: You're an optimizer, not a mathematician discovering new functions. The function FORM is fixed; tune the parameters.
