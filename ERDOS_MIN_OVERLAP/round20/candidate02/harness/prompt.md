Erdos minimum overlap: Find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

Constraint: integral(h) = 1 exactly.
Current best: C5 <= 0.38092303510845016.
Goal: Beat seed score of 0.999968 (c5_bound < 0.380923).

CRITICAL STRATEGY: The seed optimizer uses 15 diverse pattern initializations and trains for 59000 steps each.
- DON'T just generate new patterns; the optimizer already has 15.
- INSTEAD, modify HOW the optimizer works: change initialization scales, add bias terms, adjust learning dynamics.

Specific tactics:
1. Increase num_intervals from 800 to 1600 or 3200 for finer discretization
2. Adjust base_learning_rate (try 0.003, 0.01, 0.001) to change convergence
3. Modify penalty_strength (try 30, 100, 200) to affect constraint satisfaction
4. Add bias to latent (add 1.0 or -1.0 shift) to change sigmoid output distribution
5. Change num_restarts to 1 for focused search OR increase to 5 for more diversity

After each edit, call evaluate_solution and analyze the new c5_bound.
If no improvement after 3-4 edits, try completely different strategies.

Use probe_solution to screen edits cheaply before full evaluation.
