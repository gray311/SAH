Erdos minimum overlap problem (C5): Find a step function h: [0,2]->[0,1] that MINIMIZES the C5 bound.

Objective: c5_bound = max_k integral h(x)(1-h(x+k)) dx
Constraint: integral(h) = 1 exactly, h values in [0,1].
Current best: C5 <= 0.38092303510845016 (combined_score = 1.0).
GOAL: Find h with c5_bound < 0.38092303510845016 (combined_score > 1.0).

SEARCH STRATEGY (iterative refinement):
1. START with a diverse set of seed candidates (bipartite, trimodal, Golomb, uniform, sinusoidal).
2. For EACH candidate, compute its correlation structure to identify problematic shifts.
3. Apply LOCALIZED mutations: modify h in small regions to reduce overlap at the worst shifts.
4. Use ITERATIVE REFINE: after each mutation, recompute correlation and repeat steps 2-3 for 2-3 rounds.
5. Call probe_solution on refined candidates to screen.
6. Call evaluate_solution only on candidates with c5_bound < 0.382.

KEY INSIGHT: Random pattern generation fails because it wastes budget. Focus on ITERATIVE LOCAL REFINEMENT:
- Analyze current solution, find worst overlaps
- Make small targeted edits to reduce those overlaps
- Repeat refinement 2-3 times before evaluating
- This allows the solver to "home in" on improvements without random guessing.
