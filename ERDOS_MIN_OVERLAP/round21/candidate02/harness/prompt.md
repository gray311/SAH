Erdos minimum overlap problem: Find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.
Constraint: integral(h) = 1 exactly.
Current best: C5 <= 0.38092303510845016 (combined_score = 0.38092303510845016 / c5_bound).
Goal: Beat seed score 1.00001 (c5_bound < 0.3809).

STRATEGY (READ CAREFULLY):

The seed optimizer uses expensive Adam training (59000+ steps). With 30 evals total,
we CANNOT afford to train many candidates. Instead:

1. Use analyze_h_structure to rapidly prototype candidate structures. This tool
   does a quick 10-step SGD on 50-interval discretization and computes analytical c5.
   This is FAST (2-5s) and tells you if a direction is worth pursuing.

2. EDIT the EVOLVE-BLOCK to change hyperparameters for FASTER optimization:
   - REDUCE num_intervals to 200-400 (training is O(n^2) in discretization)
   - REDUCE num_steps to 10000-20000 (we'll use good initializations)
   - REDUCE penalty_strength to 10-30 (easier constraint satisfaction)
   - SET num_restarts to 5-10 (more chances with faster training)

3. After analyzing with analyze_h_structure and getting a promising candidate
   (c5 < 0.375), EDIT the program with faster hyperparameters and CALL evaluate_solution.

4. If evaluate_solution doesn't improve, try a different structure with analyze_h_structure.

5. KEY INSIGHT: Use many cheap prototypes (analyze_h_structure) to find good structures,
   then only run ONE expensive full evaluation per promising structure.

6. Expected workflow: analyze_h_structure -> (if c5<0.375) edit for faster training -> evaluate_solution.
